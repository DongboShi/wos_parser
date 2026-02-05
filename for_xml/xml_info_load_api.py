"""
XML Information Loading API

This module provides functions to load and process WOS XML files,
extracting data and writing to CSV files.
"""

import xml.etree.ElementTree as ET
import os
from xml_parser import XMLRecordParser
from csv_writer import XMLDataWriter
from xml_common_def import WOS_NAMESPACE

def load_xml_file(xml_file_path, callback_func=None):
    """
    Load and process a single XML file
    
    :param xml_file_path: Path to the XML file
    :param callback_func: Optional callback function to process each record
    :return: Number of records processed
    """
    if not os.path.exists(xml_file_path):
        print(f"Error: File not found: {xml_file_path}")
        return 0
    
    try:
        print(f"Loading XML file: {xml_file_path}")
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Find all <REC> elements
        records = root.findall('ns:REC', WOS_NAMESPACE)
        total_records = len(records)
        
        print(f"Found {total_records} records in file")
        
        processed_count = 0
        error_count = 0
        
        for idx, record in enumerate(records, 1):
            try:
                # Parse the record
                parser = XMLRecordParser(record)
                
                # Process with callback if provided
                if callback_func:
                    callback_func(parser)
                
                processed_count += 1
                
                # Progress update every 100 records
                if idx % 100 == 0:
                    print(f"Processed {idx}/{total_records} records...")
                
            except Exception as e:
                error_count += 1
                print(f"Error processing record {idx}: {str(e)}")
                continue
        
        print(f"\nCompleted processing {xml_file_path}")
        print(f"Successfully processed: {processed_count} records")
        print(f"Errors: {error_count} records")
        
        return processed_count
        
    except ET.ParseError as e:
        print(f"XML Parse Error: {str(e)}")
        return 0
    except Exception as e:
        print(f"Error loading XML file: {str(e)}")
        return 0

def load_xml_directory(directory_path, callback_func=None):
    """
    Load and process all XML files in a directory
    
    :param directory_path: Path to directory containing XML files
    :param callback_func: Optional callback function to process each record
    :return: Total number of records processed
    """
    if not os.path.exists(directory_path):
        print(f"Error: Directory not found: {directory_path}")
        return 0
    
    xml_files = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
    
    if not xml_files:
        print(f"No XML files found in {directory_path}")
        return 0
    
    print(f"Found {len(xml_files)} XML file(s) in directory")
    
    total_processed = 0
    
    for xml_file in xml_files:
        file_path = os.path.join(directory_path, xml_file)
        count = load_xml_file(file_path, callback_func)
        total_processed += count
    
    print(f"\n{'='*60}")
    print(f"Total records processed from all files: {total_processed}")
    print(f"{'='*60}")
    
    return total_processed

def process_xml_to_csv(xml_path):
    """
    Process XML file(s) and write data to CSV files
    
    :param xml_path: Path to XML file or directory containing XML files
    """
    # Initialize the CSV writer
    data_writer = XMLDataWriter()
    
    # Define callback function to write data
    def write_callback(parser):
        data_writer.write_record_data(parser)
    
    # Check if path is a file or directory
    if os.path.isfile(xml_path):
        load_xml_file(xml_path, write_callback)
    elif os.path.isdir(xml_path):
        load_xml_directory(xml_path, write_callback)
    else:
        print(f"Error: Invalid path: {xml_path}")

def filter_records_by_uid(xml_file_path, target_uids):
    """
    Filter and extract specific records by UID
    
    :param xml_file_path: Path to the XML file
    :param target_uids: List of UIDs to filter
    :return: List of matching record elements
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        matching_records = []
        
        for record in root.findall('ns:REC', WOS_NAMESPACE):
            uid_elem = record.find('ns:UID', WOS_NAMESPACE)
            if uid_elem is not None and uid_elem.text in target_uids:
                matching_records.append(record)
        
        print(f"Found {len(matching_records)} matching records")
        return matching_records
        
    except Exception as e:
        print(f"Error filtering records: {str(e)}")
        return []
