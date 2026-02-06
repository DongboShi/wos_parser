#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script showing parallel processing capabilities
Run this to see the parallel processor in action with sample data
"""

import os
import sys


def demo_handler(dict_data, data_idx, line_str, use_template, title_list):
    """Simple demo handler (must be at module level for pickling)"""
    pass


def create_demo_data():
    """Create demo WOS data files for testing"""
    demo_dir = "demo_input/sample_batch"
    os.makedirs(demo_dir, exist_ok=True)
    
    header = "PT\tAU\tTI\tSO\tPY\tVL\tIS\tBP\tEP\tPG\tTC\tZ9\tLA\tDI\tSN\tAF\tC1\tNR\tDT\tJ9\tJI\tAB\tDE\tID\tWC\tSC\tEM\tRP\tFU\tCR\tGA\tUT\tPM\tOA\tHC\tHP\tDA\tBA\tBE\tGP\tBF\tCA\tSE\tBS\tCT\tCY\tCL\tSP\tHO\tFX\tRI\tOI\tU1\tU2\tPU\tPI\tPA\tEI\tBN\tPD\tPN\tSU\tSI\tMA\tAR\tD2\tEA\n"
    
    samples = [
        "J\tSmith, J\tAI Research\tNATURE\t2023\t1\t1\t1\t10\t10\t50\t55\tEN\t10.1038/test1\t1234\tSmith, John\tMIT, USA\t20\tArticle\tNAT\tNature\tAI abstract\tAI\tML\tCS\tAI\ttest@mit.edu\tSmith\tNSF\tRef1\tGA1\tWOS:000000001\t111\t\tN\tN\t2023\t\t\t\t\t\t\t\tJ\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n",
        "J\tJones, A\tML Methods\tSCIENCE\t2023\t2\t2\t20\t30\t11\t40\t45\tEN\t10.1126/test2\t5678\tJones, Anne\tStanford, USA\t25\tArticle\tSCI\tScience\tML abstract\tML\tNN\tCS\tML\ttest@stanford.edu\tJones\tNIH\tRef2\tGA2\tWOS:000000002\t222\t\tN\tN\t2023\t\t\t\t\t\t\t\tJ\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n",
        "J\tBrown, R\tDeep Learning\tCELL\t2023\t3\t3\t30\t40\t11\t30\t35\tEN\t10.1016/test3\t9012\tBrown, Robert\tHarvard, USA\t30\tArticle\tCELL\tCell\tDL abstract\tDL\tCNN\tBio\tDL\ttest@harvard.edu\tBrown\tDOE\tRef3\tGA3\tWOS:000000003\t333\t\tN\tN\t2023\t\t\t\t\t\t\t\tJ\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n"
    ]
    
    for i, sample_data in enumerate(samples):
        filepath = os.path.join(demo_dir, f"sample_{i+1}.txt")
        with open(filepath, 'w') as f:
            f.write(header)
            f.write(sample_data)
    
    print(f"Created {len(samples)} demo files in {demo_dir}/")
    return demo_dir


def run_demo():
    """Run demonstration of parallel processing"""
    print("="*70)
    print("WOS Parser - Parallel Processing Demo")
    print("="*70)
    print()
    
    # Create demo data
    demo_dir = create_demo_data()
    print()
    
    # Demo 1: Sequential mode
    print("Demo 1: Sequential Processing Mode")
    print("-" * 70)
    from parallel_processor import ParallelFileProcessor
    
    processor = ParallelFileProcessor(worker_count=1)
    files = processor.scan_directory_tree(demo_dir)
    print(f"Found {len(files)} files to process")
    print()
    
    # Demo 2: Parallel mode
    print("Demo 2: Concurrent Processing Mode (2 workers)")
    print("-" * 70)
    from parallel_processor import process_with_concurrency
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    results = process_with_concurrency(demo_handler, "demo_input", workers=2)
    
    print()
    print("="*70)
    print("Demo completed!")
    print("="*70)
    print()
    print("To use parallel processing with your own data:")
    print("  python parser_proc_main.py --parallel")
    print("  python parser_proc_main.py --parallel --workers 4")
    print()


if __name__ == '__main__':
    run_demo()
