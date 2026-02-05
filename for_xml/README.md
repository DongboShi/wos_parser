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
```bash
python xml_proc_main.py --input [XML_FILE_PATH] --output [OUTPUT_DIR]
```
### Programmatic Usage  
```python
from xml_info_load_api import load_xml
from csv_writer import write_csv

parsed_data = load_xml('file.xml')
write_csv(parsed_data, 'output.csv')
```

## Incremental Processing Feature  
The incremental processing feature allows users to process new XML files without reprocessing already parsed files, significantly enhancing performance for large datasets.

## Additional Information  
For more details and ongoing updates, refer to the documentation or contact the maintainers of the WOS XML Parser.