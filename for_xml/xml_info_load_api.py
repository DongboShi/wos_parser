import xml.etree.ElementTree as ET
import os
from xml_parser import XMLRecordParser
from csv_writer import XMLDataWriter
from xml_common_def import WOS_NAMESPACE
from xml_processing_history import ProcessingHistoryManager


# SOLUTION 1: Define callback at module level (top-level function)
def write_record_callback(parser):
    """Callback function to write record data to CSV"""
    # Create a new writer instance in each worker process
    data_writer = XMLDataWriter()
    data_writer.write_record_data(parser)


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
    # Initialize history manager
    history_manager = ProcessingHistoryManager()
    
    # Use the module-level callback function (picklable!)
    callback_func = write_record_callback
    
    # Check if input is a file or directory
    if os.path.isfile(xml_path):
        load_xml_file(xml_path, callback_func, skip_processed, history_manager)
    elif os.path.isdir(xml_path):
        load_xml_directory(xml_path, callback_func, skip_processed, history_manager)
    else:
        raise ValueError(f"{xml_path} is neither a file nor a directory")


def process_xml_to_csv_parallel(xml_path, workers=None, skip_processed=True):
    """Process XML files in parallel mode"""
    from xml_parallel_processor import XMLParallelFileProcessor
    
    # Use the module-level callback function (picklable!)
    callback_func = write_record_callback
    
    processor = XMLParallelFileProcessor(worker_count=workers)
    
    if os.path.isfile(xml_path):
        # For single file, use sequential processing
        history_manager = ProcessingHistoryManager()
        load_xml_file(xml_path, callback_func, skip_processed, history_manager)
    elif os.path.isdir(xml_path):
        # For directory, use parallel batch processing
        processor.run_batch(callback_func, xml_path, skip_processed)
    else:
        raise ValueError(f"{xml_path} is neither a file nor a directory")


def process_xml_to_csv_fresh(xml_path):
    """Process all files fresh, ignoring processing history"""
    return process_xml_to_csv(xml_path, skip_processed=False)