import unittest
import os
import csv
from xml.etree.ElementTree import Element, SubElement, tostring
from wos_parser import XMLRecordParser

class TestXMLRecordParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Create sample XML data for testing."""
        cls.xml_data = cls.generate_sample_xml()
        cls.parser = XMLRecordParser()
        cls.output_csv = 'output.csv'
    
    @classmethod
    def generate_sample_xml(cls):
        """Generate a sample XML string for testing."""
        root = Element('root')
        record = SubElement(root, 'record')
        title = SubElement(record, 'title')
        title.text = 'Sample Title'
        author = SubElement(record, 'author')
        author.text = 'John Doe'
        return tostring(root, encoding='unicode')
    
    def test_xml_record_parser(self):
        """Test XMLRecordParser with sample XML data."""
        records = self.parser.parse(self.xml_data)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['title'], 'Sample Title')
        self.assertEqual(records[0]['author'], 'John Doe')
    
    def test_csv_output(self):
        """Test CSV output from parsed XML data."""
        records = self.parser.parse(self.xml_data)
        with open(self.output_csv, mode='w', newline='') as csvfile:
            fieldnames = ['title', 'author']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        
        # Validate the CSV output
        with open(self.output_csv, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_data = [row for row in reader]
            self.assertEqual(len(csv_data), 1)
            self.assertEqual(csv_data[0]['title'], 'Sample Title')
            self.assertEqual(csv_data[0]['author'], 'John Doe')

    @classmethod
    def tearDownClass(cls):
        """Clean up files created during tests."""
        if os.path.exists(cls.output_csv):
            os.remove(cls.output_csv)

if __name__ == '__main__':
    unittest.main()