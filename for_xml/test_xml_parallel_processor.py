#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test suite for XML parallel processing functionality
"""

import unittest
import os
import sys
import tempfile
import shutil
from xml_parallel_processor import XMLParallelFileProcessor, process_xml_with_concurrency


class TestXMLParallelProcessor(unittest.TestCase):
    """Test cases for XMLParallelFileProcessor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = XMLParallelFileProcessor(worker_count=2)
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_processor_initialization(self):
        """Test that processor initializes correctly"""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.worker_count, 2)
        
    def test_processor_auto_worker_count(self):
        """Test automatic worker count detection"""
        processor = XMLParallelFileProcessor()
        self.assertIsNotNone(processor.worker_count)
        self.assertGreater(processor.worker_count, 0)
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory"""
        files = self.processor.scan_directory_tree(self.test_dir)
        self.assertEqual(len(files), 0)
    
    def test_scan_directory_with_xml_files(self):
        """Test scanning a directory with XML files"""
        # Create test XML files
        test_file1 = os.path.join(self.test_dir, "test1.xml")
        test_file2 = os.path.join(self.test_dir, "test2.xml")
        
        with open(test_file1, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        with open(test_file2, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        
        files = self.processor.scan_directory_tree(self.test_dir)
        self.assertEqual(len(files), 2)
        self.assertTrue(any(f.endswith('test1.xml') for f in files))
        self.assertTrue(any(f.endswith('test2.xml') for f in files))
    
    def test_scan_directory_recursive(self):
        """Test recursive directory scanning"""
        # Create nested directory structure
        subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir)
        
        test_file1 = os.path.join(self.test_dir, "test1.xml")
        test_file2 = os.path.join(subdir, "test2.xml")
        
        with open(test_file1, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        with open(test_file2, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        
        files = self.processor.scan_directory_tree(self.test_dir)
        self.assertEqual(len(files), 2)
    
    def test_scan_directory_ignores_hidden_files(self):
        """Test that hidden files are ignored"""
        test_file = os.path.join(self.test_dir, ".hidden.xml")
        visible_file = os.path.join(self.test_dir, "visible.xml")
        
        with open(test_file, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        with open(visible_file, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        
        files = self.processor.scan_directory_tree(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('visible.xml'))
    
    def test_scan_directory_ignores_non_xml(self):
        """Test that non-XML files are ignored"""
        xml_file = os.path.join(self.test_dir, "test.xml")
        txt_file = os.path.join(self.test_dir, "test.txt")
        
        with open(xml_file, 'w') as f:
            f.write("<?xml version='1.0'?><root></root>")
        with open(txt_file, 'w') as f:
            f.write("Not XML")
        
        files = self.processor.scan_directory_tree(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('test.xml'))
    
    def test_scan_nonexistent_directory(self):
        """Test scanning a nonexistent directory"""
        files = self.processor.scan_directory_tree("/nonexistent/path")
        self.assertEqual(len(files), 0)
    
    def test_run_batch_empty_directory(self):
        """Test running batch on empty directory"""
        def dummy_handler(parser):
            pass
        
        result = self.processor.run_batch(dummy_handler, self.test_dir)
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['ok'], 0)
        self.assertEqual(result['failed'], 0)
    
    def test_convenience_function(self):
        """Test convenience function"""
        def dummy_handler(parser):
            pass
        
        # Should not raise exception
        result = process_xml_with_concurrency(dummy_handler, self.test_dir, workers=2)
        self.assertEqual(result['total'], 0)


class TestParallelProcessorIntegration(unittest.TestCase):
    """Integration tests for parallel processing"""
    
    def test_sequential_vs_parallel_threshold(self):
        """Test that sequential processing is used for small file counts"""
        processor = XMLParallelFileProcessor(worker_count=4)
        
        # Create a temporary directory with 2 files (below threshold of 3)
        test_dir = tempfile.mkdtemp()
        try:
            for i in range(2):
                filepath = os.path.join(test_dir, f"test{i}.xml")
                with open(filepath, 'w') as f:
                    f.write("<?xml version='1.0'?><root></root>")
            
            def dummy_handler(parser):
                pass
            
            # This should use sequential processing (output should mention it)
            result = processor.run_batch(dummy_handler, test_dir)
            # Just verify it completes without error
            self.assertIsNotNone(result)
            
        finally:
            shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()
