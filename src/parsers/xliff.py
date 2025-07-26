"""A simple XLIFF/SDLXLIFF document wrapper using lxml.objectify for perfect roundtrip parsing.

Uses lxml.objectify to automatically convert XML to Python objects, providing simple
access to all elements and attributes while preserving perfect structure.
"""

from collections.abc import Generator
from typing import Self

from lxml import etree, objectify


class XliffDocument:
    """XLIFF document wrapper using lxml.objectify for automatic XML object conversion."""

    def __init__(self, root: objectify.ObjectifiedElement):
        """Initialize with an objectified XML root element."""
        self.root = root

    @classmethod
    def from_file(cls, file_path: str) -> Self:
        """Parse XLIFF file using lxml.objectify.

        Args:
            file_path: Path to XLIFF file

        Returns:
            XliffDocument with objectified XML structure

        """
        doc = objectify.parse(file_path)
        return cls(doc.getroot())

    def to_file(self, file_path: str) -> None:
        """Write XLIFF document to file.

        Args:
            file_path: Output file path

        """
        # Clean up objectify annotations for cleaner output
        objectify.deannotate(self.root, cleanup_namespaces=True)

        with open(file_path, "wb") as f:
            f.write(etree.tostring(self.root, xml_declaration=True, encoding="UTF-8"))

    @property
    def version(self) -> str | None:
        """Get XLIFF version from root attributes."""
        return self.root.attrib.get("version")

    @property
    def xmlns(self) -> str | None:
        """Get default namespace from root attributes."""
        return self.root.nsmap.get(None)

    def get_translation_units(self) ->Generator[objectify.ObjectifiedElement, None, None]:
        """Yield all translation units in the document.

        Yields:
            objectify elements representing trans-unit elements

        """
        for file_elem in self.root.file:
            yield from file_elem.body["trans-unit"]

    def get_files(self) -> Generator[objectify.ObjectifiedElement, None, None]:
        """Yield all file elements in the document.

        Yields:
            objectify elements representing file elements

        """
        yield from self.root.file
