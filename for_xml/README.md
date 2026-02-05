# WOS XML Parser

## Project Overview  
The WOS XML Parser is a tool designed to extract data from XML files, extracting relevant information and converting it into CSV format for detailed analysis and reporting.

## Architecture Diagram  
Below is an ASCII diagram representing the module relationships within the WOS XML Parser:
```
                       +---------------------------+
                       |      xml_proc_main.py     |
                       +---------------------------+
                                 |
                                 |
         +-----------------------+-------------------------+
         |                       |                         |
 +---------------------+  +--------------------+  +--------------------+  
 | xml_info_load_api.py|  |  xml_parser.py     |  |  csv_writer.py     |  
 +---------------------+  +--------------------+  +--------------------+  
         |
         |
 +---------------------+  
 |xml_processing_history.py|
 +---------------------+
         |
         |
 +---------------------+  
 |  xml_common_def.py  |
 +---------------------+
```  

## Module Descriptions  
- **xml_proc_main.py**: The entry point for executing the XML parsing process. Controls the flow of execution and integrates various components.
- **xml_info_load_api.py**: Handles loading XML file metadata and interactions with the external data with the APIs.
- **xml_parser.py**: Implements the logic to parse the XML content into structured data that can be processed further.
- **csv_writer.py**: Responsible for writing parsed data into the desired CSV format, ensuring proper formatting and structure.
- **xml_processing_history.py**: Maintains a log of the processing history and results, allowing for reference and debugging.
- **xml_common_def.py**: Contains common definitions and utility functions shared across various modules.

## Data Flow Diagram  
The data flow for processing XML files is illustrated below:
```
[XML Files] --> [xml_info_load_api.py] --> [xml_parser.py] --> [csv_writer.py]
```  

## Processing Workflow  
1. Load XML Files using `xml_info_load_api.py`.
2. Pass the loaded data to `xml_parser.py` for parsing.
3. Write the parsed data into CSV files using `csv_writer.py`.
4. Log the processed history in `xml_processing_history.py`.

## CSV Output Structure  
The processing generates a total of 33 output CSV files, each containing specific fields and records based on the extracted XML data. A detailed structure of these files will be provided in future updates.

## Usage Examples  
### Command-Line Usage  
The parser supports processing both individual XML files and directories. When processing a directory, it will **recursively** search for all XML files in the directory and its subdirectories.

Process a single XML file:
```bash
python xml_proc_main.py path/to/file.xml
```

Process all XML files in a directory (including subdirectories):
```bash
python xml_proc_main.py path/to/directory/
```

Example with nested directory structure:
```bash
# This will process all XML files in data/ and any subdirectories
python xml_proc_main.py data/
# For example:
#   data/2023/SCI.xml
#   data/2023/AHCI.xml
#   data/2024/Q1/BSCI.xml
#   data/2024/Q2/SSCI.xml
```

### Programmatic Usage  
```python
from xml_info_load_api import process_xml_to_csv

# Process a single file
process_xml_to_csv('file.xml')

# Process a directory recursively (finds all XML files in subdirectories)
process_xml_to_csv('data_directory/')

# Process without incremental mode (reprocess all files)
from xml_info_load_api import process_xml_to_csv_fresh
process_xml_to_csv_fresh('data_directory/')
```

## Incremental Processing Feature  
The incremental processing feature allows users to process new XML files without reprocessing already parsed files, significantly enhancing performance for large datasets.

## Testing

### Running the Test Suite

The `test_xml_parser.py` file contains comprehensive unit tests for the XMLRecordParser. These tests validate the XML parsing functionality using sample data from the `examples` directory.

#### Basic Usage

To run all tests:
```bash
cd for_xml
python test_xml_parser.py
```

#### Running with Verbose Output

For detailed test results:
```bash
python test_xml_parser.py -v
```

#### Running Specific Test Cases

Run a specific test class:
```bash
python test_xml_parser.py TestXMLRecordParser
```

Run a specific test method:
```bash
python test_xml_parser.py TestXMLRecordParser.test_uid_extraction
```

Run tests matching a pattern (Python 3.7+):
```bash
python test_xml_parser.py -k extract_item
```

#### Other Useful Options

- `-f` or `--failfast`: Stop on the first failure
- `-b` or `--buffer`: Buffer stdout and stderr during tests
- `-q` or `--quiet`: Minimal output
- `--locals`: Show local variables in tracebacks

#### Test Structure

The test suite is organized into three main test classes:

1. **TestXMLRecordParser**: Core functionality tests for the XMLRecordParser class
   - Tests UID extraction
   - Tests all extraction methods (item, title, abstract, authors, etc.)
   - Tests data consistency

2. **TestXMLParserWithDifferentEditions**: Tests parsing of different WOS edition files
   - AHCI, BHCI, BSCI, ESCI, ISSHP, ISTP, SCI, SSCI editions

3. **TestXMLParserComprehensive**: Comprehensive validation of all extraction methods
   - Tests all Section 1 extractors (Paper Basic Information)
   - Tests all Section 2 extractors (Author Information)
   - Tests all Section 3 extractors (Category Information)
   - Tests all Section 4 extractors (References)
   - Tests all Section 5 extractors (Funding Information)
   - Tests all Section 6 extractors (Conference Information)

#### Prerequisites

The tests require:
- Python 3.x
- Sample XML files in the `examples` directory (already included)
- The `xml_parser.py` and `xml_common_def.py` modules in the same directory

#### Example Test Output

```bash
$ python test_xml_parser.py -v
test_ahci_edition (test_xml_parser.TestXMLParserWithDifferentEditions) ... ok
test_uid_extraction (test_xml_parser.TestXMLRecordParser) ... ok
...
----------------------------------------------------------------------
Ran 30 tests in 0.015s

OK (skipped=2)
```

## Additional Information  
For more details and ongoing updates, refer to the documentation or contact the maintainers of the WOS XML Parser.