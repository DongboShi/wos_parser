"""
Unit tests for XMLRecordParser

Tests the XML parsing functionality for Web of Science (WOS) XML records.
Uses sample XML data from the examples directory to validate parsing.
"""

import unittest
import os
import xml.etree.ElementTree as ET
from xml_parser import XMLRecordParser
from xml_common_def import WOS_NAMESPACE


class TestXMLRecordParser(unittest.TestCase):
    """Test cases for XMLRecordParser class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures using example XML files."""
        cls.ns = WOS_NAMESPACE
        # Load a sample XML file for testing
        cls.example_xml_path = os.path.join(os.path.dirname(__file__), 'examples', 'SCI.xml')
        cls.tree = ET.parse(cls.example_xml_path)
        cls.root = cls.tree.getroot()
        # Get the first REC element for testing
        cls.record = cls.root.find('.//ns:REC', cls.ns)
        cls.parser = XMLRecordParser(cls.record)
    
    def test_uid_extraction(self):
        """Test that UID is correctly extracted from record."""
        self.assertIsNotNone(self.parser.uid)
        self.assertTrue(self.parser.uid.startswith('WOS:'))
    
    def test_extract_item(self):
        """Test extraction of item (basic paper information)."""
        item = self.parser.extract_item()
        self.assertIsNotNone(item)
        self.assertEqual(item['uid'], self.parser.uid)
        self.assertIn('sortdate', item)
        self.assertIn('pubyear', item)
        self.assertIn('vol', item)
    
    def test_extract_item_title(self):
        """Test extraction of item title."""
        title = self.parser.extract_item_title()
        self.assertIsNotNone(title)
        self.assertEqual(title['uid'], self.parser.uid)
        self.assertIn('title', title)
        self.assertTrue(len(title['title']) > 0)
    
    def test_extract_item_abstract(self):
        """Test extraction of item abstract."""
        abstract = self.parser.extract_item_abstract()
        # Abstract may or may not exist in the record
        if abstract is not None:
            self.assertEqual(abstract['uid'], self.parser.uid)
            self.assertIn('abstract', abstract)
    
    def test_extract_item_doc_types(self):
        """Test extraction of document types."""
        doctypes = self.parser.extract_item_doc_types()
        if doctypes is not None:
            self.assertIsInstance(doctypes, list)
            for doctype in doctypes:
                self.assertEqual(doctype['uid'], self.parser.uid)
                self.assertIn('doctype', doctype)
    
    def test_extract_item_editions(self):
        """Test extraction of editions."""
        editions = self.parser.extract_item_editions()
        if editions is not None:
            self.assertIsInstance(editions, list)
            for edition in editions:
                self.assertEqual(edition['uid'], self.parser.uid)
                self.assertIn('edition', edition)
    
    def test_extract_item_keywords(self):
        """Test extraction of keywords."""
        keywords = self.parser.extract_item_keywords()
        if keywords is not None:
            self.assertIsInstance(keywords, list)
            for keyword in keywords:
                self.assertEqual(keyword['uid'], self.parser.uid)
                self.assertIn('keyword', keyword)
    
    def test_extract_item_source(self):
        """Test extraction of item source."""
        source = self.parser.extract_item_source()
        self.assertIsNotNone(source)
        self.assertEqual(source['uid'], self.parser.uid)
        self.assertIn('source', source)
    
    def test_extract_item_authors(self):
        """Test extraction of authors."""
        authors = self.parser.extract_item_authors()
        if authors is not None:
            self.assertIsInstance(authors, list)
            self.assertGreater(len(authors), 0)
            for author in authors:
                self.assertEqual(author['uid'], self.parser.uid)
                self.assertIn('seq_no', author)
                self.assertIn('display_name', author)
    
    def test_extract_item_addresses(self):
        """Test extraction of addresses."""
        addresses = self.parser.extract_item_addresses()
        if addresses is not None:
            self.assertIsInstance(addresses, list)
            for address in addresses:
                self.assertEqual(address['uid'], self.parser.uid)
                self.assertIn('addr_no', address)
    
    def test_extract_item_orgs(self):
        """Test extraction of organizations."""
        orgs = self.parser.extract_item_orgs()
        if orgs is not None:
            self.assertIsInstance(orgs, list)
            for org in orgs:
                self.assertEqual(org['uid'], self.parser.uid)
                self.assertIn('addr_no', org)
                self.assertIn('organization', org)
    
    def test_extract_item_references(self):
        """Test extraction of references."""
        references = self.parser.extract_item_references()
        if references is not None:
            self.assertIsInstance(references, list)
            for reference in references:
                self.assertEqual(reference['uid'], self.parser.uid)
                self.assertIn('occurence_order', reference)
    
    def test_extract_item_grants(self):
        """Test extraction of grants."""
        grants = self.parser.extract_item_grants()
        if grants is not None:
            self.assertIsInstance(grants, list)
            for grant in grants:
                self.assertEqual(grant['uid'], self.parser.uid)
    
    def test_multiple_records(self):
        """Test parsing multiple records from an XML file."""
        records = self.root.findall('.//ns:REC', self.ns)
        self.assertGreater(len(records), 0)
        
        for record in records:
            parser = XMLRecordParser(record)
            self.assertIsNotNone(parser.uid)
            
            # Test that basic extraction works for each record
            item = parser.extract_item()
            self.assertIsNotNone(item)
            self.assertEqual(item['uid'], parser.uid)


class TestXMLParserWithDifferentEditions(unittest.TestCase):
    """Test XMLRecordParser with different edition XML files"""
    
    def test_bhci_edition(self):
        """Test parsing BHCI edition XML file."""
        xml_path = os.path.join(os.path.dirname(__file__), 'examples', 'BHCI.xml')
        if os.path.exists(xml_path):
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                record = root.find('.//ns:REC', WOS_NAMESPACE)
                if record is not None:
                    parser = XMLRecordParser(record)
                    self.assertIsNotNone(parser.uid)
                    item = parser.extract_item()
                    self.assertIsNotNone(item)
            except ET.ParseError:
                # BHCI.xml may contain multiple XML documents
                # Skip this test if the file is malformed
                self.skipTest("BHCI.xml contains multiple XML documents")
    
    def test_istp_edition(self):
        """Test parsing ISTP edition XML file."""
        xml_path = os.path.join(os.path.dirname(__file__), 'examples', 'ISTP.xml')
        if os.path.exists(xml_path):
            tree = ET.parse(xml_path)
            root = tree.getroot()
            record = root.find('.//ns:REC', WOS_NAMESPACE)
            if record is not None:
                parser = XMLRecordParser(record)
                self.assertIsNotNone(parser.uid)
                item = parser.extract_item()
                self.assertIsNotNone(item)


if __name__ == '__main__':
    unittest.main()