import pytest
import tempfile
import os
from lxml import etree

from parsers.xliff import XliffDocument


@pytest.fixture
def xliff_file_path():
    return os.path.join(os.path.dirname(__file__), "testdata", "basic.xlf")


@pytest.fixture
def sdl_xliff_file_path():
    return os.path.join(os.path.dirname(__file__), "testdata", "test_sample.sdlxliff")


def test_from_file(xliff_file_path):
    doc = XliffDocument.from_file(xliff_file_path)
    assert doc is not None
    assert doc.version == "1.2"
    assert doc.xmlns == "urn:oasis:names:tc:xliff:document:1.2"


def test_from_file_not_found():
    with pytest.raises(OSError):
        XliffDocument.from_file("non_existent_file.xlf")


def test_from_file_invalid_xml():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".xlf", encoding="utf-8") as f:
        f.write("<xliff><unclosed-tag>")
        f.seek(0)
        with pytest.raises(etree.XMLSyntaxError):
            XliffDocument.from_file(f.name)


def test_get_files(xliff_file_path):
    doc = XliffDocument.from_file(xliff_file_path)
    files = list(doc.get_files())
    assert len(files) == 1
    assert files[0].attrib["original"] == "file.ext"


def test_get_translation_units(xliff_file_path):
    doc = XliffDocument.from_file(xliff_file_path)
    units = list(doc.get_translation_units())
    assert len(units) == 2
    assert str(units[0].source) == "Hello world"
    assert str(units[1].target) == "Une autre chaîne"


def test_to_file_roundtrip(xliff_file_path):
    doc = XliffDocument.from_file(xliff_file_path)
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".xlf") as f:
        output_path = f.name
    doc.to_file(output_path)

    assert os.path.exists(output_path)

    doc2 = XliffDocument.from_file(output_path)
    assert doc.version == doc2.version
    assert doc.xmlns == doc2.xmlns

    units1 = list(doc.get_translation_units())
    units2 = list(doc2.get_translation_units())
    assert len(units1) == len(units2)
    for u1, u2 in zip(units1, units2):
        assert str(u1.source) == str(u2.source)
        assert str(u1.target) == str(u2.target)

    os.remove(output_path)


def test_from_sdl_file(sdl_xliff_file_path):
    doc = XliffDocument.from_file(sdl_xliff_file_path)
    assert doc is not None
    assert doc.version == "1.2"
    assert doc.xmlns == "urn:oasis:names:tc:xliff:document:1.2"
    units = list(doc.get_translation_units())
    assert len(units) == 2
    assert units[0].source == '<source>Hello, <g id="1" ctype="x-html-em">world</g>!</source>'
    assert units[0].target == '<target state="translated" origin="tm" match-quality="95">¡Hola, <g id="1" ctype="x-html-em">mundo</g>!</target>'
    assert units[1].source == '<source>This is a test document with <g id="1" ctype="x-html-strong">formatting</g>.</source>'
    assert units[1].target == '<target state="needs-translation"/>'
