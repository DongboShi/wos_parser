# Incremental Processing Feature Documentation

## Overview
The Incremental Processing feature allows users to skip already processed XML records, making it easier to manage large datasets without duplicating efforts. This feature is particularly useful for ongoing or routine processing of XML records.

**NEW: The parser now supports recursive directory processing**, automatically finding and processing XML files in subdirectories. This works seamlessly with incremental processing to track files across the entire directory tree.

## Usage Instructions

### Using the Command-Line Tool

The simplest way to use incremental processing is through the command-line interface:

```bash
# First run - processes all XML files in directory and subdirectories
python xml_proc_main.py /path/to/xml/directory/

# Second run - skips already processed files and records
python xml_proc_main.py /path/to/xml/directory/
```

The processing history is automatically saved in `processing_history.json` in the current directory.

### Programmatic Usage

```python
from xml_info_load_api import process_xml_to_csv, process_xml_to_csv_fresh

# Process with incremental mode (default - skips already processed records)
process_xml_to_csv('/path/to/xml/directory/', skip_processed=True)

# Process fresh (reprocess all files, ignore history)
process_xml_to_csv_fresh('/path/to/xml/directory/')
```

### Step 1: Configure Your Environment
Ensure that your environment is set up correctly to handle XML processing. This may include installing necessary libraries and configuring your XML parser.

### Step 2: Processing History Management
The processing history is automatically managed in `processing_history.json`. You can:

- View processing statistics:
  ```bash
  python xml_processing_history.py summary
  ```

- Export a detailed report:
  ```bash
  python xml_processing_history.py report
  ```

- Reset history (to reprocess all files):
  ```bash
  python xml_processing_history.py reset
  ```

### Step 3: Recursive Directory Processing
When you provide a directory path, the parser will:
1. Recursively walk through all subdirectories
2. Find all `.xml` files at any depth
3. Process each file and track it in the history
4. Skip files that have already been processed on subsequent runs

### Step 5: Test Your Setup
Run your processing setup on a sample of XML records to ensure that already processed records are being skipped properly.

## Example
Here is a sample pseudo-code demonstrating the incremental processing:
```python
processed_records = set(load_processed_records())

for record in xml_records:
    if record.id not in processed_records:
        process_record(record)
        processed_records.add(record.id)
```

## Conclusion
By following these steps, you can efficiently use the Incremental Processing feature in your XML processing workflow. This will save time and resources by avoiding duplication of work.

For more information or specific use cases, please refer to additional documentation or contact support.