"""
XML Processing Main Entry Point

This script is the main entry point for processing WOS XML files.
It extracts data from XML files and writes them to CSV files.

Usage:
    python xml_proc_main.py <path_to_xml_file_or_directory>
"""

import sys
import os
from xml_info_load_api import process_xml_to_csv
from xml_common_def import OUTPUT_DIR

def main():
    """Main function to process XML files"""
    
    print("="*60)
    print("WOS XML Parser - CSV Extraction Tool")
    print("="*60)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\nUsage: python xml_proc_main.py <path_to_xml_file_or_directory>")
        print("\nExample:")
        print("  python xml_proc_main.py data/SCI.xml")
        print("  python xml_proc_main.py data/xml_files/")
        sys.exit(1)
    
    xml_path = sys.argv[1]
    
    # Verify path exists
    if not os.path.exists(xml_path):
        print(f"\nError: Path does not exist: {xml_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"\nCreated output directory: {OUTPUT_DIR}")
    
    print(f"\nInput: {xml_path}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nStarting XML processing...\n")
    
    # Process the XML files
    try:
        process_xml_to_csv(xml_path)
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