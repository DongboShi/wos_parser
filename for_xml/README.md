# WOS XML Parser

## Description
The WOS XML Parser is a Python library designed to process and parse Web of Science (WOS) XML export files. It extracts relevant information and structures it in a way that is easy to work with and analyze.

## Features
- Efficient parsing of WOS XML files
- Data extraction capabilities
- Support for various WOS XML schemas

## Installation
You can install the WOS XML Parser by using pip:

```bash
pip install wos_parser
```

## Usage
To use the WOS XML Parser, import the library and utilize its functions:

```python
from wos_parser import parse

parsed_data = parse('file.xml')
```

## Incremental Processing Capabilities
The WOS XML Parser now includes support for incremental processing. This feature allows users to process large XML files in smaller chunks, reducing memory usage and improving performance.

### How It Works
- The incremental processing feature reads the XML file in sections, parsing and extracting data as each section is read. 
- Users can now analyze data incrementally, making it suitable for handling very large datasets that cannot fit into memory all at once.

### Example Usage
Here’s a short example demonstrating how to utilize incremental processing:

```python
from wos_parser import incremental_parse

for parsed_chunk in incremental_parse('large_file.xml'):
    # Process each chunk of parsed data
    handle_data(parsed_chunk)
```

## xml_processing_history.py Module
The `xml_processing_history.py` module keeps track of the history of processed XML files and their corresponding metadata.

### Features of xml_processing_history.py
- Maintain a log of all processed XML files.
- Record metadata such as file size, number of records, and processing time.
- Allow users to review historical processing data for auditing or performance evaluation.

### Usage Example
To use `xml_processing_history.py`, you can do the following:

```python
from wos_parser.history import log_processing

log_processing(file_name='processed_file.xml', size=50000, records=1000, duration=30)
```

## Conclusion
The WOS XML Parser is a powerful tool for parsing WOS XML files, now enhanced with incremental processing capabilities. This enhancement allows users to work efficiently with large datasets while maintaining a detailed history of their processing activities.