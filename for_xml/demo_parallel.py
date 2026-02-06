#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script for XML parallel processing
This demonstrates how to use the parallel processing capabilities for XML files
"""

import os
import sys


def demo_sequential():
    """Demonstrate sequential XML processing"""
    print("="*70)
    print("Demo 1: Sequential XML Processing")
    print("="*70)
    print("\nCommand:")
    print("  python xml_proc_main.py data/")
    print("\nThis processes XML files one at a time in sequential order.")
    print("Best for: Small numbers of files or single file processing")
    print()


def demo_parallel():
    """Demonstrate parallel XML processing"""
    print("="*70)
    print("Demo 2: Parallel XML Processing")
    print("="*70)
    print("\nCommand:")
    print("  python xml_proc_main.py data/ --parallel")
    print("\nThis processes multiple XML files concurrently using multiple workers.")
    print("Best for: Processing 3+ XML files for improved performance")
    print()


def demo_parallel_with_workers():
    """Demonstrate parallel processing with specific worker count"""
    print("="*70)
    print("Demo 3: Parallel Processing with Specific Worker Count")
    print("="*70)
    print("\nCommand:")
    print("  python xml_proc_main.py data/ --parallel --workers 4")
    print("\nThis uses exactly 4 worker processes.")
    print("Best for: Fine-tuning performance based on your system resources")
    print()


def demo_fresh_processing():
    """Demonstrate fresh processing (ignore history)"""
    print("="*70)
    print("Demo 4: Fresh Processing (Ignore History)")
    print("="*70)
    print("\nCommand:")
    print("  python xml_proc_main.py data/ --parallel --no-skip-processed")
    print("\nThis reprocesses all files, ignoring the processing history.")
    print("Best for: Reprocessing data after fixing errors or updating logic")
    print()


def demo_programmatic():
    """Demonstrate programmatic usage"""
    print("="*70)
    print("Demo 5: Programmatic Usage")
    print("="*70)
    print("\nPython code:")
    print("""
from xml_info_load_api import process_xml_to_csv_parallel

# Process with default settings (auto-detect workers)
process_xml_to_csv_parallel('data_directory/')

# Process with 4 workers
process_xml_to_csv_parallel('data_directory/', workers=4)

# Process without skipping (fresh processing)
process_xml_to_csv_parallel('data_directory/', skip_processed=False)

# Combine options
process_xml_to_csv_parallel('data_directory/', workers=8, skip_processed=False)
""")
    print()


def main():
    """Run all demos"""
    print("\n")
    print("*"*70)
    print("XML Parallel Processing Demo")
    print("*"*70)
    print("\nThis demo shows different ways to use the XML parallel processor.")
    print()
    
    demo_sequential()
    demo_parallel()
    demo_parallel_with_workers()
    demo_fresh_processing()
    demo_programmatic()
    
    print("="*70)
    print("Performance Tips")
    print("="*70)
    print("""
1. Use --parallel for 3+ XML files to maximize throughput
2. For 1-2 files, sequential mode is automatically used (more efficient)
3. Worker count defaults to your CPU count (optimal for most cases)
4. Each worker processes complete XML files independently
5. Use --skip-processed (default) to avoid reprocessing files
6. Use --no-skip-processed to force reprocessing of all files
""")
    
    print("="*70)
    print("For more information, see README.md")
    print("="*70)


if __name__ == "__main__":
    main()
