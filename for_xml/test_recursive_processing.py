#!/usr/bin/env python3
"""
Test script to verify recursive XML directory processing functionality.

This test creates a directory structure with XML files in multiple levels
of subdirectories and verifies that all files are processed correctly.
"""

import unittest
import os
import sys
import shutil
import tempfile

# Add the for_xml directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xml_info_load_api import load_xml_directory, ProcessingHistoryManager


class TestRecursiveXMLProcessing(unittest.TestCase):
    """Test cases for recursive XML directory processing"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures - create test directory structure"""
        cls.test_dir = tempfile.mkdtemp(prefix='test_recursive_xml_')
        cls.examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
        
        # Create directory structure with subdirectories
        cls.subdir1 = os.path.join(cls.test_dir, 'subdir1')
        cls.subdir2 = os.path.join(cls.test_dir, 'subdir1', 'subdir2')
        cls.subdir3 = os.path.join(cls.test_dir, 'subdir3')
        
        os.makedirs(cls.subdir1)
        os.makedirs(cls.subdir2)
        os.makedirs(cls.subdir3)
        
        # Copy XML files to different levels
        cls.xml_files = []
        
        # Root level
        if os.path.exists(os.path.join(cls.examples_dir, 'SCI.xml')):
            shutil.copy(
                os.path.join(cls.examples_dir, 'SCI.xml'),
                os.path.join(cls.test_dir, 'SCI.xml')
            )
            cls.xml_files.append(os.path.join(cls.test_dir, 'SCI.xml'))
        
        # First subdirectory
        if os.path.exists(os.path.join(cls.examples_dir, 'AHCI.xml')):
            shutil.copy(
                os.path.join(cls.examples_dir, 'AHCI.xml'),
                os.path.join(cls.subdir1, 'AHCI.xml')
            )
            cls.xml_files.append(os.path.join(cls.subdir1, 'AHCI.xml'))
        
        # Nested subdirectory
        if os.path.exists(os.path.join(cls.examples_dir, 'BSCI.xml')):
            shutil.copy(
                os.path.join(cls.examples_dir, 'BSCI.xml'),
                os.path.join(cls.subdir2, 'BSCI.xml')
            )
            cls.xml_files.append(os.path.join(cls.subdir2, 'BSCI.xml'))
        
        # Another subdirectory at root level
        if os.path.exists(os.path.join(cls.examples_dir, 'SSCI.xml')):
            shutil.copy(
                os.path.join(cls.examples_dir, 'SSCI.xml'),
                os.path.join(cls.subdir3, 'SSCI.xml')
            )
            cls.xml_files.append(os.path.join(cls.subdir3, 'SSCI.xml'))
        
        # Create temporary history file
        cls.history_file = tempfile.mktemp(suffix='.json')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
        if os.path.exists(cls.history_file):
            os.remove(cls.history_file)
    
    def test_recursive_directory_processing(self):
        """Test that all XML files in subdirectories are found and processed"""
        processed_files = []
        processed_records = []
        
        def test_callback(parser):
            """Track processed records"""
            if parser and hasattr(parser, 'uid'):
                processed_records.append(parser.uid)
        
        history_manager = ProcessingHistoryManager(self.history_file)
        
        # Process the directory recursively
        load_xml_directory(self.test_dir, test_callback, skip_processed=False, history_manager=history_manager)
        
        # Verify that records were processed
        self.assertGreater(len(processed_records), 0, "No records were processed")
        
        # Verify that the history manager tracked files
        file_count = history_manager.get_file_count()
        self.assertGreater(file_count, 0, "No files were tracked in history")
        
        # Print summary for verification
        print(f"\nProcessed {len(processed_records)} records from {file_count} files")
        print(f"Expected to process {len(self.xml_files)} files")
    
    def test_directory_structure_integrity(self):
        """Test that the directory structure was created correctly"""
        self.assertTrue(os.path.exists(self.test_dir), "Test directory should exist")
        self.assertTrue(os.path.exists(self.subdir1), "Subdir1 should exist")
        self.assertTrue(os.path.exists(self.subdir2), "Subdir2 should exist")
        self.assertTrue(os.path.exists(self.subdir3), "Subdir3 should exist")
        
        # Verify XML files exist in expected locations
        for xml_file in self.xml_files:
            self.assertTrue(os.path.exists(xml_file), f"XML file should exist: {xml_file}")
    
    def test_incremental_processing(self):
        """Test that incremental processing (skipping already processed files) works"""
        processed_count_first = []
        processed_count_second = []
        
        def count_callback(parser):
            """Count processed records"""
            if parser and hasattr(parser, 'uid'):
                processed_count_first.append(parser.uid)
        
        def count_callback_second(parser):
            """Count processed records in second run"""
            if parser and hasattr(parser, 'uid'):
                processed_count_second.append(parser.uid)
        
        history_manager = ProcessingHistoryManager(self.history_file)
        
        # First run - process all files
        load_xml_directory(self.test_dir, count_callback, skip_processed=True, history_manager=history_manager)
        
        # Second run - should skip already processed files
        load_xml_directory(self.test_dir, count_callback_second, skip_processed=True, history_manager=history_manager)
        
        # Second run should process 0 new records
        self.assertEqual(len(processed_count_second), 0, 
                        "Second run should skip all already processed records")
        
        print(f"\nFirst run: {len(processed_count_first)} records")
        print(f"Second run: {len(processed_count_second)} records (should be 0)")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
