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
- **xml_proc_main.py**: The entry point for executing the XML parsing process. Controls the flow of execution and integrates various components. Supports both sequential and parallel processing modes.
- **xml_info_load_api.py**: Handles loading XML file metadata and interactions with the external data with the APIs. Provides both sequential and parallel processing functions.
- **xml_parser.py**: Implements the logic to parse the XML content into structured data that can be processed further.
- **csv_writer.py**: Responsible for writing parsed data into the desired CSV format, ensuring proper formatting and structure.
- **xml_processing_history.py**: Maintains a log of the processing history and results, allowing for reference and debugging.
- **xml_parallel_processor.py**: Provides concurrent processing capabilities using multiprocessing to efficiently handle large numbers of XML files.
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

#### Sequential Processing (Default)
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

#### Parallel Processing Mode
For improved performance when processing large numbers of XML files, enable parallel processing with the `--parallel` flag:

```bash
# Enable parallel processing with auto-detected worker count
python xml_proc_main.py data/ --parallel

# Specify number of workers
python xml_proc_main.py data/ --parallel --workers 4

# Parallel processing with fresh reprocessing (ignore history)
python xml_proc_main.py data/ --parallel --no-skip-processed
```

**Performance Notes:**
- Parallel processing is most effective with 3+ XML files
- For 1-2 files, sequential processing is automatically used
- Worker count defaults to CPU count if not specified
- Each worker processes complete XML files independently

### Programmatic Usage  
#### Sequential Processing
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

#### Parallel Processing
```python
from xml_info_load_api import process_xml_to_csv_parallel

# Process directory with parallel workers (auto-detect worker count)
process_xml_to_csv_parallel('data_directory/')

# Specify worker count
process_xml_to_csv_parallel('data_directory/', workers=4)

# Disable incremental processing (reprocess all files)
process_xml_to_csv_parallel('data_directory/', skip_processed=False)

# Combine options
process_xml_to_csv_parallel('data_directory/', workers=8, skip_processed=False)
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

## Importing CSV Data to MySQL Database

After generating CSV files, you can import them into a MySQL or MariaDB database for easier querying and analysis.

### Quick Start

**Option 1: Using the convenience script (recommended)**
```bash
# Import using the bash script
./import_csv_to_mysql.sh [mysql_password] [database_name]

# Example
./import_csv_to_mysql.sh mypassword wos_xml
```

**Option 2: Using SQL commands directly**

1. Create database and tables:
   ```bash
   mysql -u root -p < create_database_and_tables.sql
   # OR for MariaDB
   mariadb -u root -p < create_database_and_tables.sql
   ```

2. Import CSV data:
   ```bash
   mysql -u root -p --local-infile=1 < import_csv_data.sql
   # OR for MariaDB
   mariadb -u root -p --local-infile=1 < import_csv_data.sql
   ```

This will:
- Create a MySQL/MariaDB database named `wos_xml`
- Create 33 tables with proper schema and indexes
- Import all CSV files from the `xml_output` directory

### Custom Configuration

The bash script supports environment variables:
```bash
# Specify custom host and database
DB_HOST=myserver DB_NAME=my_wos_db ./import_csv_to_mysql.sh mypassword

# Specify custom CSV directory
CSV_DIR=my_csv_dir ./import_csv_to_mysql.sh mypassword wos_xml
```

For direct SQL usage, edit the SQL files to customize database name and paths.

### Exploring the Data

After import, run example queries:
```bash
python example_queries.py
```

This demonstrates common analysis queries including paper statistics, author rankings, citation patterns, and more.

Note: Running example queries requires pymysql:
```bash
pip install -r requirements_mysql.txt
```

### Detailed Documentation

For comprehensive information about MySQL import, including:
- Database schema details
- Advanced configuration options
- Querying examples
- Troubleshooting guide

See [MYSQL_IMPORT_GUIDE.md](MYSQL_IMPORT_GUIDE.md)

## Additional Information  
For more details and ongoing updates, refer to the documentation or contact the maintainers of the WOS XML Parser.