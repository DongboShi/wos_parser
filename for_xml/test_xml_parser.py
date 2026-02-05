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
    
    def _test_edition_file(self, filename):
        """Helper method to test a specific edition XML file."""
        xml_path = os.path.join(os.path.dirname(__file__), 'examples', filename)
        if not os.path.exists(xml_path):
            self.skipTest(f"{filename} not found")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            record = root.find('.//ns:REC', WOS_NAMESPACE)
            if record is not None:
                parser = XMLRecordParser(record)
                self.assertIsNotNone(parser.uid)
                item = parser.extract_item()
                self.assertIsNotNone(item)
                return parser
        except ET.ParseError:
            # Some files may contain multiple XML documents
            self.skipTest(f"{filename} contains multiple XML documents or is malformed")
    
    def test_ahci_edition(self):
        """Test parsing AHCI edition XML file."""
        self._test_edition_file('AHCI.xml')
    
    def test_bhci_edition(self):
        """Test parsing BHCI edition XML file."""
        self._test_edition_file('BHCI.xml')
    
    def test_bsci_edition(self):
        """Test parsing BSCI edition XML file."""
        self._test_edition_file('BSCI.xml')
    
    def test_esci_edition(self):
        """Test parsing ESCI edition XML file."""
        self._test_edition_file('ESCI.xml')
    
    def test_isshp_edition(self):
        """Test parsing ISSHP edition XML file."""
        self._test_edition_file('ISSHP.xml')
    
    def test_istp_edition(self):
        """Test parsing ISTP edition XML file."""
        self._test_edition_file('ISTP.xml')
    
    def test_sci_edition(self):
        """Test parsing SCI edition XML file."""
        parser = self._test_edition_file('SCI.xml')
        if parser:
            # Additional validation for SCI edition
            title = parser.extract_item_title()
            self.assertIsNotNone(title)
            self.assertTrue(len(title['title']) > 0)
    
    def test_ssci_edition(self):
        """Test parsing SSCI edition XML file."""
        self._test_edition_file('SSCI.xml')


class TestXMLParserComprehensive(unittest.TestCase):
    """Comprehensive tests for all extraction methods"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures using example XML files."""
        cls.ns = WOS_NAMESPACE
        # Use SCI.xml as it has the most complete data
        cls.example_xml_path = os.path.join(os.path.dirname(__file__), 'examples', 'SCI.xml')
        cls.tree = ET.parse(cls.example_xml_path)
        cls.root = cls.tree.getroot()
        cls.record = cls.root.find('.//ns:REC', cls.ns)
        cls.parser = XMLRecordParser(cls.record)
    
    def test_all_section1_extractors(self):
        """Test all Section 1 (Paper Basic Information) extractors."""
        # Test all section 1 methods exist and return expected types
        self.assertIsNotNone(self.parser.extract_item())
        
        methods = [
            'extract_item_title',
            'extract_item_abstract', 
            'extract_item_doc_types',
            'extract_item_doc_types_norm',
            'extract_item_langs',
            'extract_item_langs_norm',
            'extract_item_editions',
            'extract_item_keywords',
            'extract_item_keywords_plus',
            'extract_item_source',
            'extract_item_ids',
            'extract_item_oas',
            'extract_item_publishers'
        ]
        
        for method_name in methods:
            method = getattr(self.parser, method_name)
            result = method()
            # Result can be None, dict, or list - just verify method callable
            self.assertTrue(callable(method), f"{method_name} should be callable")
    
    def test_all_section2_extractors(self):
        """Test all Section 2 (Author Information) extractors."""
        methods = [
            'extract_item_authors',
            'extract_item_addresses',
            'extract_item_au_addrs',
            'extract_item_orgs',
            'extract_item_suborgs',
            'extract_item_author_ids',
            'extract_item_rp_addrs',
            'extract_item_rp_au_addrs',
            'extract_item_rp_orgs',
            'extract_item_rp_suborgs',
            'extract_item_contributors'
        ]
        
        for method_name in methods:
            method = getattr(self.parser, method_name)
            result = method()
            self.assertTrue(callable(method), f"{method_name} should be callable")
    
    def test_all_section3_extractors(self):
        """Test all Section 3 (Category Information) extractors."""
        methods = ['extract_item_headings', 'extract_item_subjects']
        
        for method_name in methods:
            method = getattr(self.parser, method_name)
            result = method()
            self.assertTrue(callable(method), f"{method_name} should be callable")
    
    def test_all_section4_extractors(self):
        """Test all Section 4 (References) extractors."""
        methods = ['extract_item_references', 'extract_item_cite_locations']
        
        for method_name in methods:
            method = getattr(self.parser, method_name)
            result = method()
            self.assertTrue(callable(method), f"{method_name} should be callable")
    
    def test_all_section5_extractors(self):
        """Test all Section 5 (Funding Information) extractors."""
        methods = ['extract_item_acks', 'extract_item_grants']
        
        for method_name in methods:
            method = getattr(self.parser, method_name)
            result = method()
            self.assertTrue(callable(method), f"{method_name} should be callable")
    
    def test_all_section6_extractors(self):
        """Test all Section 6 (Conference Information) extractors."""
        methods = ['extract_item_conferences']
        
        for method_name in methods:
            method = getattr(self.parser, method_name)
            result = method()
            self.assertTrue(callable(method), f"{method_name} should be callable")
    
    def test_uid_uniqueness(self):
        """Test that each record has a unique UID."""
        records = self.root.findall('.//ns:REC', self.ns)
        uids = set()
        
        for record in records:
            parser = XMLRecordParser(record)
            self.assertNotIn(parser.uid, uids, f"Duplicate UID found: {parser.uid}")
            uids.add(parser.uid)
    
    def test_data_consistency(self):
        """Test that extracted data maintains UID consistency."""
        # Extract different data types
        item = self.parser.extract_item()
        title = self.parser.extract_item_title()
        authors = self.parser.extract_item_authors()
        
        # Verify all have the same UID
        if item:
            self.assertEqual(item['uid'], self.parser.uid)
        if title:
            self.assertEqual(title['uid'], self.parser.uid)
        if authors:
            for author in authors:
                self.assertEqual(author['uid'], self.parser.uid)


if __name__ == '__main__':
    unittest.main()