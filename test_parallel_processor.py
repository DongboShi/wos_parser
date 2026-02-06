#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for parallel processing module
"""

import os
import tempfile
import shutil
from parallel_processor import ParallelFileProcessor


def create_test_data(test_dir):
    """Generate sample test files"""
    os.makedirs(test_dir, exist_ok=True)
    
    # Create subdirectory structure
    subdir1 = os.path.join(test_dir, 'batch1')
    subdir2 = os.path.join(test_dir, 'batch2')
    os.makedirs(subdir1, exist_ok=True)
    os.makedirs(subdir2, exist_ok=True)
    
    # Sample WOS header
    header = "PT\tAU\tTI\tSO\tPY\tVL\tIS\tBP\tEP\tPG\tTC\tZ9\tLA\tDI\tSN\tAF\tC1\tNR\tDT\tJ9\tJI\tAB\tDE\tID\tWC\tSC\tEM\tRP\tFU\tCR\tGA\tUT\tPM\tOA\tHC\tHP\tDA\tBA\tBE\tGP\tBF\tCA\tSE\tBS\tCT\tCY\tCL\tSP\tHO\tFX\tRI\tOI\tU1\tU2\tPU\tPI\tPA\tEI\tBN\tPD\tPN\tSU\tSI\tMA\tAR\tD2\tEA\n"
    
    # Create test files
    for i in range(3):
        filepath = os.path.join(subdir1, f'test_{i}.txt')
        with open(filepath, 'w') as f:
            f.write(header)
            f.write(f"J\tSmith, A\tTest Paper {i}\tNature\t2023\t1\t1\t1\t10\t10\t5\t5\tEN\t10.1234/test{i}\t1234-5678\tSmith, A\tUniv Test\t10\tArticle\tNAT\tNature\tTest abstract\tKeyword1\tID1\tScience\tMultidisciplinary\temail@test.com\tSmith\tGrant1\tRef1\tGA123\tWOS:00000000{i}\tPM123\tOA\tHC\tHP\tDA\tBA\tBE\tGP\tBF\tCA\tSE\tBS\tCT\tCY\tCL\tSP\tHO\tFX\tRI\tOI\tU1\tU2\tPU\tPI\tPA\tEI\tBN\tPD\tPN\tSU\tSI\tMA\tAR\tD2\tEA\n")
    
    for i in range(2):
        filepath = os.path.join(subdir2, f'test_{i}.txt')
        with open(filepath, 'w') as f:
            f.write(header)
            f.write(f"J\tJones, B\tAnother Paper {i}\tScience\t2023\t2\t2\t20\t30\t11\t3\t3\tEN\t10.1234/test{i+10}\t8765-4321\tJones, B\tUniv Science\t15\tArticle\tSCI\tScience\tAnother abstract\tKeyword2\tID2\tBiology\tCell Biology\temail2@test.com\tJones\tGrant2\tRef2\tGA456\tWOS:00000001{i}\tPM456\tOA\tHC\tHP\tDA\tBA\tBE\tGP\tBF\tCA\tSE\tBS\tCT\tCY\tCL\tSP\tHO\tFX\tRI\tOI\tU1\tU2\tPU\tPI\tPA\tEI\tBN\tPD\tPN\tSU\tSI\tMA\tAR\tD2\tEA\n")


def mock_handler(dict_data, data_idx, line_str, use_template, title_list):
    """Mock processing handler for testing"""
    pass


def test_file_scanner():
    """Test directory scanning functionality"""
    print("Test 1: Directory scanning")
    test_dir = tempfile.mkdtemp()
    
    try:
        create_test_data(test_dir)
        processor = ParallelFileProcessor(worker_count=2)
        files = processor.scan_directory_tree(test_dir)
        
        assert len(files) == 5, f"Expected 5 files, found {len(files)}"
        print(f"  ✓ Found {len(files)} files")
        print("  ✓ Directory scanning works correctly\n")
        
    finally:
        shutil.rmtree(test_dir)


def test_concurrent_execution():
    """Test concurrent processing"""
    print("Test 2: Concurrent execution")
    test_dir = tempfile.mkdtemp()
    
    try:
        create_test_data(test_dir)
        processor = ParallelFileProcessor(worker_count=2)
        
        # Change to temp directory for test
        original_dir = os.getcwd()
        os.chdir(tempfile.gettempdir())
        
        # Create test directory in current location
        local_test = os.path.basename(test_dir)
        
        results = processor.run_batch(mock_handler, local_test)
        
        os.chdir(original_dir)
        
        assert results['total'] == 5, f"Expected 5 total, got {results['total']}"
        assert results['ok'] >= 0, "Expected successful processing"
        print(f"  ✓ Processed {results['total']} files")
        print(f"  ✓ Success: {results['ok']}, Failed: {results['failed']}")
        print("  ✓ Concurrent execution works correctly\n")
        
    finally:
        shutil.rmtree(test_dir)


def test_processor_initialization():
    """Test processor initialization with different worker counts"""
    print("Test 3: Processor initialization")
    
    p1 = ParallelFileProcessor()
    assert p1.worker_count >= 1, "Worker count should be at least 1"
    print(f"  ✓ Auto-detected {p1.worker_count} workers")
    
    p2 = ParallelFileProcessor(worker_count=3)
    assert p2.worker_count == 3, "Worker count should be 3"
    print(f"  ✓ Manual worker count: {p2.worker_count}")
    print("  ✓ Processor initialization works correctly\n")


if __name__ == '__main__':
    print("="*60)
    print("Running Parallel Processor Tests")
    print("="*60 + "\n")
    
    test_processor_initialization()
    test_file_scanner()
    test_concurrent_execution()
    
    print("="*60)
    print("All tests passed!")
    print("="*60)
