#!/usr/bin/env python3
"""
Split large WOS XML.gz files into smaller chunks for parallel processing

This script:
1. Decompresses .xml.gz files
2. Splits them into smaller XML files (each containing N records)
3. Optionally compresses the chunks back to .xml.gz
4. Saves them to a specified output directory

Usage:
    python split_xml_gz.py input.xml.gz --records-per-file 1000 --output-dir chunks/
    python split_xml_gz.py input.xml.gz -r 500 -o chunks/ --compress
"""

import argparse
import gzip
import os
import xml.etree.ElementTree as ET
from pathlib import Path


def split_xml_gz(input_file, output_dir, records_per_file=1000, compress=False, verbose=True):
    """
    Split a large XML.gz file into smaller XML files
    
    :param input_file: Path to input .xml.gz file
    :param output_dir: Directory to save split files
    :param records_per_file: Number of records per split file
    :param compress: Whether to compress output files to .xml.gz
    :param verbose: Print progress information
    """
    
    if verbose:
        print(f"=" * 60)
        print(f"Splitting: {input_file}")
        print(f"Records per file: {records_per_file}")
        print(f"Output directory: {output_dir}")
        print(f"Compress output: {compress}")
        print(f"=" * 60)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract base filename
    base_name = Path(input_file).stem  # Remove .gz
    if base_name.endswith('.xml'):
        base_name = base_name[:-4]  # Remove .xml
    
    # Step 1: Decompress and parse XML
    if verbose:
        print("\n[1/3] Decompressing and parsing XML...")
    
    try:
        if input_file.endswith('.gz'):
            with gzip.open(input_file, 'rt', encoding='utf-8') as f:
                tree = ET.parse(f)
        else:
            tree = ET.parse(input_file)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return
    
    root = tree.getroot()
    
    # Find namespace
    ns = ''
    if root.tag.startswith('{'):
        ns = root.tag.split('}')[0] + '}'
    
    # Find all REC elements
    records = root.findall(f'{ns}REC')
    total_records = len(records)
    
    if verbose:
        print(f"      Found {total_records} records")
    
    if total_records == 0:
        print("Warning: No records found in file!")
        return
    
    # Step 2: Split records into chunks
    if verbose:
        print(f"\n[2/3] Splitting into chunks...")
    
    num_chunks = (total_records + records_per_file - 1) // records_per_file
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * records_per_file
        end_idx = min(start_idx + records_per_file, total_records)
        chunk_records = records[start_idx:end_idx]
        
        # Create new XML structure
        new_root = ET.Element(root.tag, root.attrib)
        
        # Copy namespace declarations
        for key, value in root.attrib.items():
            if key.startswith('xmlns'):
                new_root.set(key, value)
        
        # Add records to new root
        for record in chunk_records:
            new_root.append(record)
        
        # Generate output filename
        chunk_filename = f"{base_name}_part{chunk_idx+1:04d}.xml"
        if compress:
            chunk_filename += ".gz"
        
        output_path = os.path.join(output_dir, chunk_filename)
        
        # Write chunk
        new_tree = ET.ElementTree(new_root)
        ET.indent(new_tree, space='    ')  # Pretty print (Python 3.9+)
        
        try:
            if compress:
                with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                    new_tree.write(f, encoding='unicode', xml_declaration=True)
            else:
                new_tree.write(output_path, encoding='utf-8', xml_declaration=True)
            
            if verbose:
                # Print on same line with carriage return
                print(f"\r      Creating chunks: {chunk_idx+1}/{num_chunks} - {chunk_filename} ({len(chunk_records)} records)", end='', flush=True)
        
        except Exception as e:
            print(f"\nError writing {output_path}: {e}")
            return
    
    # Print newline after loop completes
    if verbose:
        print()  # Move to next line after progress
    
    # Step 3: Summary
    if verbose:
        print(f"\n[3/3] Summary:")
        print(f"      Input file: {input_file}")
        print(f"      Total records: {total_records}")
        print(f"      Output files: {num_chunks}")
        print(f"      Records per file: {records_per_file}")
        print(f"      Output directory: {output_dir}")
        print(f"\n" + "=" * 60)
        print(f"Splitting complete!")
        print(f"=" * 60)
        print(f"\nTo process these files:")
        print(f"python xml_proc_main.py {output_dir} --parallel --workers 4")


def split_multiple_files(input_files, output_base_dir, records_per_file=1000, compress=False, verbose=True):
    """
    Split multiple XML.gz files
    
    :param input_files: List of input file paths
    :param output_base_dir: Base directory for output
    :param records_per_file: Number of records per split file
    :param compress: Whether to compress output files
    :param verbose: Print progress information
    """
    
    print(f"\n{'=' * 60}")
    print(f"Batch splitting {len(input_files)} files")
    print(f"{'=' * 60}\n")
    
    for i, input_file in enumerate(input_files, 1):
        print(f"\n[{i}/{len(input_files)}] Processing: {input_file}")
        
        # Create subdirectory for each file
        base_name = Path(input_file).stem
        if base_name.endswith('.xml'):
            base_name = base_name[:-4]
        
        file_output_dir = os.path.join(output_base_dir, base_name)
        
        split_xml_gz(
            input_file,
            file_output_dir,
            records_per_file,
            compress,
            verbose
        )


def main():
    parser = argparse.ArgumentParser(
        description='Split large WOS XML.gz files into smaller chunks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split a single file (1000 records per chunk)
  python split_xml_gz.py WR_1980_CORE_0001.xml.gz -r 1000 -o chunks/
  
  # Split with compression
  python split_xml_gz.py WR_1980_CORE_0001.xml.gz -r 500 -o chunks/ --compress
  
  # Split all files in a directory
  python split_xml_gz.py /data/wos/ -r 1000 -o /data/wos_chunks/
  
  # Keep original directory structure
  python split_xml_gz.py /data/wos/1980_CORE/file.xml.gz -r 1000 -o /data/chunks/
  # Output: /data/chunks/1980_CORE/file/part****.xml
  
  # Then process the chunks
  python xml_proc_main.py /data/wos_chunks/ --parallel --workers 4
        """
    )
    
    parser.add_argument('input', 
                       help='Input XML.gz file or directory containing XML.gz files')
    parser.add_argument('-o', '--output-dir', 
                       default='xml_chunks',
                       help='Output directory for split files (default: xml_chunks)')
    parser.add_argument('-r', '--records-per-file', 
                       type=int, 
                       default=1000,
                       help='Number of records per split file (default: 1000)')
    parser.add_argument('-c', '--compress', 
                       action='store_true',
                       help='Compress output files to .xml.gz')
    parser.add_argument('-q', '--quiet', 
                       action='store_true',
                       help='Suppress verbose output')
    parser.add_argument('-k', '--keep-structure', 
                       action='store_true',
                       help='Keep original directory structure in output')
    
    args = parser.parse_args()
    
    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Single file
        if args.keep_structure:
            # Keep directory structure
            # Extract relative path components
            input_path = Path(args.input)
            
            # Get the filename without .gz
            stem = input_path.stem  # Remove .gz
            if stem.endswith('.xml'):
                stem = stem[:-4]  # Remove .xml
            
            # Get parent directory name (e.g., 1980_CORE)
            parent_dir = input_path.parent.name
            
            # Create output path: output-dir/parent-dir/filename/
            if parent_dir and parent_dir != '.':
                file_output_dir = os.path.join(args.output_dir, parent_dir, stem)
            else:
                file_output_dir = os.path.join(args.output_dir, stem)
        else:
            # Use output-dir directly
            file_output_dir = args.output_dir
        
        split_xml_gz(
            args.input,
            file_output_dir,
            args.records_per_file,
            args.compress,
            not args.quiet
        )
    
    elif os.path.isdir(args.input):
        # Directory - find all .xml.gz files
        xml_gz_files = []
        for root, dirs, files in os.walk(args.input):
            for file in files:
                if file.endswith('.xml.gz'):
                    xml_gz_files.append(os.path.join(root, file))
        
        if not xml_gz_files:
            print(f"No .xml.gz files found in {args.input}")
            return
        
        print(f"Found {len(xml_gz_files)} .xml.gz files in {args.input}")
        
        if args.keep_structure:
            # Process each file, keeping directory structure
            for i, input_file in enumerate(xml_gz_files, 1):
                print(f"\n[{i}/{len(xml_gz_files)}] Processing: {input_file}")
                
                # Get relative path from input directory
                rel_path = os.path.relpath(input_file, args.input)
                rel_dir = os.path.dirname(rel_path)
                
                # Get filename without extension
                base_name = Path(input_file).stem
                if base_name.endswith('.xml'):
                    base_name = base_name[:-4]
                
                # Create output path preserving structure
                if rel_dir:
                    file_output_dir = os.path.join(args.output_dir, rel_dir, base_name)
                else:
                    file_output_dir = os.path.join(args.output_dir, base_name)
                
                split_xml_gz(
                    input_file,
                    file_output_dir,
                    args.records_per_file,
                    args.compress,
                    not args.quiet
                )
        else:
            # Process all files into flat output directory
            split_multiple_files(
                xml_gz_files,
                args.output_dir,
                args.records_per_file,
                args.compress,
                not args.quiet
            )
    
    else:
        print(f"Error: {args.input} does not exist")
        return


if __name__ == "__main__":
    main()
