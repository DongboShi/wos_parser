"""
XML Processing Main Entry Point

This script is the main entry point for processing WOS XML files.
It extracts data from XML files and writes them to CSV files.

Usage:
    python xml_proc_main.py <path_to_xml_file_or_directory> [--parallel] [--workers N] [--skip-processed]
"""

import sys
import os
import argparse
from xml_info_load_api import process_xml_to_csv, process_xml_to_csv_parallel
from xml_common_def import OUTPUT_DIR

def main():
    """Main function to process XML files"""
    
    print("="*60)
    print("WOS XML Parser - CSV Extraction Tool")
    print("="*60)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='WOS XML Parser - Process Web of Science XML data',
        epilog='Examples:\n'
               '  python xml_proc_main.py data/SCI.xml\n'
               '  python xml_proc_main.py data/xml_files/\n'
               '  python xml_proc_main.py data/xml_files/ --parallel\n'
               '  python xml_proc_main.py data/xml_files/ --parallel --workers 4',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('xml_path', help='Path to XML file or directory')
    parser.add_argument('--parallel', action='store_true', 
                       help='Enable concurrent processing')
    parser.add_argument('--workers', type=int, default=None,
                       help='Worker count for parallel mode (default: auto-detect)')
    parser.add_argument('--skip-processed', dest='skip_processed', action='store_true', default=True,
                       help='Skip already processed files (default: True)')
    parser.add_argument('--no-skip-processed', dest='skip_processed', action='store_false',
                       help='Reprocess all files, ignoring history')
    
    args = parser.parse_args()
    
    # Verify path exists
    if not os.path.exists(args.xml_path):
        print(f"\nError: Path does not exist: {args.xml_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"\nCreated output directory: {OUTPUT_DIR}")
    
    print(f"\nInput: {args.xml_path}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Process the XML files
    try:
        if args.parallel:
            print("==> Concurrent processing mode active")
            if args.workers:
                print(f"==> Using {args.workers} workers")
            print("\nStarting XML processing...\n")
            process_xml_to_csv_parallel(args.xml_path, workers=args.workers, skip_processed=args.skip_processed)
        else:
            print("==> Sequential processing mode active")
            print("\nStarting XML processing...\n")
            process_xml_to_csv(args.xml_path, skip_processed=args.skip_processed)
        
        print("\n" + "="*60)
        print("Processing completed successfully!")
        print(f"CSV files have been saved to: {OUTPUT_DIR}")
        print("="*60)
        
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()