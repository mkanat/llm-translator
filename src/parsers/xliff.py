"""
A simple XLIFF/SDLXLIFF document wrapper using lxml.objectify for perfect roundtrip parsing

Uses lxml.objectify to automatically convert XML to Python objects, providing simple
access to all elements and attributes while preserving perfect structure.
"""

from typing import Optional
from lxml import objectify, etree
import logging

logger = logging.getLogger(__name__)


class XliffDocument:
    """XLIFF document wrapper using lxml.objectify for automatic XML object conversion"""
    
    def __init__(self, root: objectify.ObjectifiedElement):
        """Initialize with an objectified XML root element"""
        self.root = root
    
    @classmethod
    def from_file(cls, file_path: str) -> 'XliffDocument':
        """
        Parse XLIFF file using lxml.objectify
        
        Args:
            file_path: Path to XLIFF file
            
        Returns:
            XliffDocument with objectified XML structure
        """
        doc = objectify.parse(file_path)
        root = doc.getroot()
        
        logger.info(f"Parsed XLIFF document: {file_path}")
        return cls(root)
    
    def to_file(self, file_path: str) -> None:
        """
        Write XLIFF document to file
        
        Args:
            file_path: Output file path
        """
        # Clean up objectify annotations for cleaner output
        objectify.deannotate(self.root)
        etree.cleanup_namespaces(self.root)
        
        with open(file_path, 'wb') as f:
            f.write(etree.tostring(
                self.root, 
                pretty_print=True, 
                xml_declaration=True, 
                encoding='UTF-8'
            ))
        
        logger.info(f"Wrote XLIFF document: {file_path}")
    
    @property
    def version(self) -> Optional[str]:
        """Get XLIFF version from root attributes"""
        return self.root.attrib.get('version')
    
    @property 
    def xmlns(self) -> Optional[str]:
        """Get default namespace from root attributes"""
        return self.root.attrib.get('xmlns')
    
    def get_translation_units(self):
        """
        Generator that yields all translation units in the document
        
        Yields:
            objectify elements representing trans-unit elements
        """
        for file_elem in self.root.file:
            for trans_unit in file_elem.body['trans-unit']:
                yield trans_unit
    
    def get_files(self):
        """
        Generator that yields all file elements in the document
        
        Yields:
            objectify elements representing file elements  
        """
        for file_elem in self.root.file:
            yield file_elem