import pytest
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


def test_from_file_invalid_xml(tmp_path):
    invalid_file = tmp_path / "invalid.xlf"
    invalid_file.write_text("<xliff><unclosed-tag>")
    with pytest.raises(etree.XMLSyntaxError):
        XliffDocument.from_file(str(invalid_file))


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


def test_to_file_roundtrip(xliff_file_path, tmp_path):
    doc = XliffDocument.from_file(xliff_file_path)
    output_path = tmp_path / "roundtrip.xlf"
    doc.to_file(str(output_path))

    assert output_path.exists()

    doc2 = XliffDocument.from_file(str(output_path))
    assert doc.version == doc2.version
    assert doc.xmlns == doc2.xmlns

    units1 = list(doc.get_translation_units())
    units2 = list(doc2.get_translation_units())
    assert len(units1) == len(units2)
    for u1, u2 in zip(units1, units2):
        assert str(u1.source) == str(u2.source)
        assert str(u1.target) == str(u2.target)


def test_parse_sdlxliff(sdl_xliff_file_path):
    doc = XliffDocument.from_file(sdl_xliff_file_path)
    assert doc.version == "1.2"
    assert doc.xmlns == "urn:oasis:names:tc:xliff:document:1.2"

    files = list(doc.get_files())
    assert len(files) == 1
    file_elem = files[0]
    assert file_elem.attrib["original"] == "test.txt"
    assert file_elem.attrib["source-language"] == "en-US"
    assert file_elem.attrib["target-language"] == "es-ES"
    assert file_elem.attrib["datatype"] == "x-sdlfilterframework2"

    units = list(doc.get_translation_units())
    assert len(units) == 2

    # First translation unit
    u1 = units[0]
    # Source with emphasis tag
    assert u1.source.text == "Hello, "
    g = u1.source.getchildren()[0]
    assert g.tag.split("}")[-1] == "g"
    assert g.attrib["ctype"] == "x-html-em"
    assert g.text == "world"
    assert g.tail == "!"
    # Target with emphasis tag
    assert u1.target.text == "¡Hola, "
    gt = u1.target.getchildren()[0]
    assert gt.tag.split("}")[-1] == "g"
    assert gt.attrib["ctype"] == "x-html-em"
    assert gt.text == "mundo"
    assert gt.tail == "!"
    assert str(u1.note) == "Greeting with emphasis"

    alt = u1.find("alt-trans")
    assert alt is not None
    assert str(alt.source) == "Hello, world!"
    assert str(alt.target) == "Hola mundo!"

    # Second translation unit
    u2 = units[1]
    assert "This is a test document" in str(u2.source)
    assert str(u2.target) == ""
