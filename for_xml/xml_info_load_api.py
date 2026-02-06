import xml.etree.ElementTree as ET
import os
from xml_parser import XMLRecordParser
from csv_writer import XMLDataWriter
from xml_common_def import WOS_NAMESPACE
from xml_processing_history import ProcessingHistoryManager


# Module-level callback for parallel processing
# This needs to be at module level to be picklable for multiprocessing
def _write_record_to_csv(parser):
    """
    Module-level callback function for writing record data to CSV.
    Creates its own XMLDataWriter instance for use in parallel processing.
    This function must be at module level to be picklable for multiprocessing.
    """
    # Each worker process creates its own writer
    # This is safe because CSV writes are append operations
    from csv_writer import XMLDataWriter
    writer = XMLDataWriter()
    writer.write_record_data(parser)


def load_xml_file(xml_file_path, callback_func, skip_processed, history_manager):
    """Load and process a single XML file with incremental processing support"""
    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"The file {xml_file_path} does not exist.")
    
    # Skip if already processed and skip_processed is enabled
    if skip_processed and history_manager.is_file_processed(xml_file_path):
        print(f"Skipping already processed file: {xml_file_path}")
        return
    
    print(f"Processing file: {xml_file_path}")
    
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Find all REC elements (records)
        records = root.findall('.//ns:REC', WOS_NAMESPACE)
        
        record_count = 0
        error_count = 0
        
        # Process each record
        for record in records:
            try:
                parser = XMLRecordParser(record)
                
                # Skip if already processed and skip_processed is enabled
                if skip_processed and history_manager.is_record_processed(parser.uid):
                    continue
                
                # Call the callback function with the parser
                callback_func(parser)
                
                # Mark record as processed
                history_manager.mark_record_processed(parser.uid, xml_file_path)
                record_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Error processing record: {str(e)}")
                try:
                    parser = XMLRecordParser(record)
                    history_manager.mark_error(parser.uid, str(e), xml_file_path)
                except:
                    pass
        
        # Mark file as fully processed
        history_manager.mark_file_processed(xml_file_path, record_count, error_count)
        print(f"Processed {record_count} records from {xml_file_path}")
        
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file_path}: {str(e)}")
        raise
    except Exception as e:
        print(f"Error processing file {xml_file_path}: {str(e)}")
        raise


def load_xml_directory(directory_path, callback_func, skip_processed, history_manager):
    """Recursively load all XML files in the given directory and subdirectories"""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory {directory_path} does not exist.")
    
    if not os.path.isdir(directory_path):
        raise ValueError(f"{directory_path} is not a directory.")
    
    # Recursively walk through directory and all subdirectories
    for root_dir, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.xml'):
                xml_file_path = os.path.join(root_dir, filename)
                try:
                    load_xml_file(xml_file_path, callback_func, skip_processed, history_manager)
                except Exception as e:
                    print(f"Failed to process {xml_file_path}: {str(e)}")


def process_xml_to_csv(xml_path, skip_processed=True):
    """Process the XML file or directory at xml_path to CSV, handle skip_processed logic here"""
    # Initialize data writer and history manager
    data_writer = XMLDataWriter()
    history_manager = ProcessingHistoryManager()
    
    # Define callback function to write record data
    def write_callback(parser):
        data_writer.write_record_data(parser)
    
    # Check if input is a file or directory
    if os.path.isfile(xml_path):
        load_xml_file(xml_path, write_callback, skip_processed, history_manager)
    elif os.path.isdir(xml_path):
        load_xml_directory(xml_path, write_callback, skip_processed, history_manager)
    else:
        raise ValueError(f"{xml_path} is neither a file nor a directory.")
    
    # Print summary
    print("\n" + "="*60)
    print("Processing Summary")
    print("="*60)
    history_manager.print_summary()


def process_xml_to_csv_fresh(xml_path):
    """Process XML file as fresh, ignoring any processed history"""
    process_xml_to_csv(xml_path, skip_processed=False)


def filter_records_by_uid(xml_file_path, target_uids):
    """Filter records in the XML file by specific UIDs"""
    if not os.path.exists(xml_file_path):
        raise FileNotFoundError(f"The file {xml_file_path} does not exist.")
    
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        records = root.findall('.//ns:REC', WOS_NAMESPACE)
        filtered_records = []
        
        for record in records:
            parser = XMLRecordParser(record)
            if parser.uid in target_uids:
                filtered_records.append(parser)
        
        return filtered_records
        
    except Exception as e:
        print(f"Error filtering records: {str(e)}")
        raise


def reprocess_records(uids, xml_path):
    """Reprocess specific records identified by UIDs"""
    history_manager = ProcessingHistoryManager()
    
    # Remove UIDs from history to allow reprocessing
    for uid in uids:
        history_manager.remove_record(uid)
    
    # Process with skip_processed enabled (will reprocess removed UIDs)
    process_xml_to_csv(xml_path, skip_processed=True)


def process_xml_to_csv_parallel(xml_path, workers=None, skip_processed=True):
    """Process XML files using concurrent workers for improved performance"""
    from xml_parallel_processor import process_xml_with_concurrency
    
    # Check if input is a file or directory
    if os.path.isfile(xml_path):
        # For single file, use sequential processing
        print("Single file detected, using sequential processing")
        process_xml_to_csv(xml_path, skip_processed=skip_processed)
    elif os.path.isdir(xml_path):
        # For directory, use parallel processing
        # Use the module-level callback function which is picklable
        process_xml_with_concurrency(_write_record_to_csv, xml_path, workers=workers, skip_processed=skip_processed)
    else:
        raise ValueError(f"{xml_path} is neither a file nor a directory.")
