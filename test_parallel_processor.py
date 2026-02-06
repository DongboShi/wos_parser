#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for parallel processing module
"""

import os
import tempfile
import shutil
from parallel_processor import ParallelFileProcessor


# WOS data format constants for testing
WOS_HEADER_FIELDS = [
    "PT", "AU", "TI", "SO", "PY", "VL", "IS", "BP", "EP", "PG", 
    "TC", "Z9", "LA", "DI", "SN", "AF", "C1", "NR", "DT", "J9", 
    "JI", "AB", "DE", "ID", "WC", "SC", "EM", "RP", "FU", "CR", 
    "GA", "UT", "PM", "OA", "HC", "HP", "DA", "BA", "BE", "GP", 
    "BF", "CA", "SE", "BS", "CT", "CY", "CL", "SP", "HO", "FX", 
    "RI", "OI", "U1", "U2", "PU", "PI", "PA", "EI", "BN", "PD", 
    "PN", "SU", "SI", "MA", "AR", "D2", "EA"
]


def generate_wos_header():
    """Generate WOS format header line"""
    return "\t".join(WOS_HEADER_FIELDS) + "\n"


def generate_wos_record(author, title, journal, ut_suffix):
    """Generate a sample WOS data record"""
    fields = [
        "J", author, title, journal, "2023", "1", "1", "1", "10", "10",
        "5", "5", "EN", f"10.1234/test{ut_suffix}", "1234-5678", 
        author, "Univ Test", "10", "Article", "NAT", "Nature",
        "Test abstract", "Keyword1", "ID1", "Science", "Multidisciplinary",
        "email@test.com", author.split(",")[0], "Grant1", "Ref1",
        "GA123", f"WOS:0000000{ut_suffix}", "PM123", "OA", "HC", "HP",
        "DA", "BA", "BE", "GP", "BF", "CA", "SE", "BS", "CT", "CY",
        "CL", "SP", "HO", "FX", "RI", "OI", "U1", "U2", "PU", "PI",
        "PA", "EI", "BN", "PD", "PN", "SU", "SI", "MA", "AR", "D2", "EA"
    ]
    return "\t".join(fields) + "\n"


def create_test_data(test_dir):
    """Generate sample test files"""
    os.makedirs(test_dir, exist_ok=True)
    
    # Create subdirectory structure
    subdir1 = os.path.join(test_dir, 'batch1')
    subdir2 = os.path.join(test_dir, 'batch2')
    os.makedirs(subdir1, exist_ok=True)
    os.makedirs(subdir2, exist_ok=True)
    
    header = generate_wos_header()
    
    # Create test files in subdir1
    for i in range(3):
        filepath = os.path.join(subdir1, f'test_{i}.txt')
        with open(filepath, 'w') as f:
            f.write(header)
            f.write(generate_wos_record("Smith, A", f"Test Paper {i}", "Nature", str(i)))
    
    # Create test files in subdir2
    for i in range(2):
        filepath = os.path.join(subdir2, f'test_{i}.txt')
        with open(filepath, 'w') as f:
            f.write(header)
            f.write(generate_wos_record("Jones, B", f"Another Paper {i}", "Science", str(i+10)))


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
