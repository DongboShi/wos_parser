# WOS XML Parser - CSV Extraction Tool

This directory contains tools for parsing Web of Science (WOS) XML files and extracting data into structured CSV files.

## 📋 Overview

The XML parser extracts data from WOS XML files according to the table design specifications in `tables.md` and outputs the data into separate CSV files for each table.

## 🏗️ Architecture

### Core Modules

- **`xml_common_def.py`**: Defines output file paths and XML namespace constants
- **`xml_parser.py`**: Core XML record parser class that extracts data from `<REC>` elements
- **`csv_writer.py`**: CSV writing utilities with proper comma/quote escaping
- **`xml_info_load_api.py`**: API for loading and processing XML files
- **`xml_proc_main.py`**: Main entry point script

### Data Flow

```
XML File(s) → xml_info_load_api → XMLRecordParser → XMLDataWriter → CSV Files
```

## 📦 Output Structure

All CSV files are written to the `xml_output/` directory (configurable in `xml_common_def.py`).

### Output Files by Category

#### 1. Paper Basic Information (14 files)
- `item.csv` - Core paper metadata
- `item_title.csv` - Paper titles
- `item_abstract.csv` - Paper abstracts
- `item_doc_types.csv` - Document types
- `item_doc_types_norm.csv` - Normalized document types
- `item_langs.csv` - Languages
- `item_langs_norm.csv` - Normalized languages
- `item_editions.csv` - WOS editions
- `item_keywords.csv` - Author keywords
- `item_keywords_plus.csv` - Keywords Plus
- `item_source.csv` - Source/journal information
- `item_ids.csv` - Various identifiers (DOI, PMID, etc.)
- `item_oas.csv` - Open access information
- `item_publishers.csv` - Publisher information

#### 2. Author Information (11 files)
- `item_authors.csv` - Author names and details
- `item_addresses.csv` - Author addresses
- `item_au_addrs.csv` - Author-address relationships
- `item_orgs.csv` - Organizations
- `item_suborgs.csv` - Sub-organizations
- `item_author_ids.csv` - Author identifiers (ORCID, ResearcherID)
- `item_rp_addrs.csv` - Reprint author addresses
- `item_rp_au_addrs.csv` - Reprint author-address relationships
- `item_rp_orgs.csv` - Reprint organizations
- `item_rp_suborgs.csv` - Reprint sub-organizations
- `item_contributors.csv` - Contributors with IDs

#### 3. Category Information (2 files)
- `item_headings.csv` - Research field headings
- `item_subjects.csv` - Research subjects with ASCA types

#### 4. References (2 files)
- `item_references.csv` - Cited references
- `item_cite_locations.csv` - Citation locations in text

#### 5. Funding Information (2 files)
- `item_acks.csv` - Acknowledgment text
- `item_grants.csv` - Grant information

#### 6. Conference Information (1 file)
- `item_conferences.csv` - Conference details

## 🚀 Usage

### Basic Usage

Process a single XML file:

```bash
python xml_proc_main.py path/to/your/file.xml
```

Process all XML files in a directory:

```bash
python xml_proc_main.py path/to/xml_directory/
```

### Example

```bash
# Process the sample SCI.xml file
python xml_proc_main.py ../SCI.xml

# Process all XML files in a data directory
python xml_proc_main.py /data/wos_xml_files/
```

### Output

```
============================================================
WOS XML Parser - CSV Extraction Tool
============================================================

Input: ../SCI.xml
Output directory: xml_output

Starting XML processing...

Loading XML file: ../SCI.xml
Found 1 records in file

Completed processing ../SCI.xml
Successfully processed: 1 records
Errors: 0 records

============================================================
Processing completed successfully!
CSV files have been saved to: xml_output
============================================================
```

## 📊 CSV Format

- **Separator**: Comma (`,`)
- **Encoding**: UTF-8
- **Line Endings**: System default
- **Quote Character**: Double quote (`"`)
- **Quoting**: Automatic for fields containing commas, quotes, or newlines

### Example CSV Output

```csv
uid,title
WOS:000805468200001,"Human Obesity Attenuates Cardioprotection Conferred by Adipose Tissue-Derived Mesenchymal Stem/Stromal Cells"
```

Fields containing commas are automatically quoted:

```csv
uid,subject,ascatype
WOS:000805468200001,"Cardiac & Cardiovascular Systems",traditional
```

## 🔧 Programmatic Usage

### Process XML Files with Custom Callback

```python
from xml_info_load_api import load_xml_file
from xml_parser import XMLRecordParser

def my_custom_callback(parser):
    """Custom processing for each record"""
    item_data = parser.extract_item()
    print(f"Processing: {item_data['uid']}")
    # Do custom processing...

# Load and process
load_xml_file('data/SCI.xml', callback_func=my_custom_callback)
```

### Filter Records by UID

```python
from xml_info_load_api import filter_records_by_uid

# Get specific records
target_uids = ['WOS:000805468200001', 'WOS:000805468200002']
records = filter_records_by_uid('data/SCI.xml', target_uids)

# Process filtered records
for record in records:
    parser = XMLRecordParser(record)
    # ... process
```

### Extract Specific Data Only

```python
from xml_parser import XMLRecordParser
import xml.etree.ElementTree as ET

# Parse XML
tree = ET.parse('data/SCI.xml')
root = tree.getroot()

# Process first record
from xml_common_def import WOS_NAMESPACE
record = root.find('ns:REC', WOS_NAMESPACE)
parser = XMLRecordParser(record)

# Extract only what you need
title = parser.extract_item_title()
authors = parser.extract_item_authors()
references = parser.extract_item_references()
```

## 🛠️ Configuration

### Change Output Directory

Edit `xml_common_def.py`:

```python
# Change this line
OUTPUT_DIR = "xml_output"

# To your preferred directory
OUTPUT_DIR = "/path/to/output"
```

### Customize CSV File Names

Edit the file name constants in `xml_common_def.py`:

```python
ITEM_FILE_NAME = "item.csv"  # Change to "papers.csv" if desired
```

## 📝 Data Handling

### Missing Fields

According to `tables.md`, missing fields are handled as follows:

- **Required fields** (e.g., UID, pubyear): Will raise an error if missing
- **Optional fields**: Left blank (empty string) in CSV

### Multiple Values

Tables with one-to-many relationships (e.g., multiple authors per paper) create multiple rows:

```csv
uid,seq_no,full_name
WOS:000805468200001,1,"Yu, Shasha"
WOS:000805468200001,2,"Klomjit, Nattawat"
WOS:000805468200001,3,"Jiang, Kai"
```

### Special Characters

The CSV writer automatically handles:
- **Commas** in text: Field is quoted
- **Quotes** in text: Doubled (`""`)
- **Newlines** in text: Field is quoted
- **HTML entities** (e.g., `&amp;`): Preserved as-is from XML

## 🐛 Error Handling

### Common Issues

1. **File not found**
   ```
   Error: File not found: path/to/file.xml
   ```
   → Check the file path is correct

2. **XML Parse Error**
   ```
   XML Parse Error: not well-formed (invalid token)
   ```
   → Check XML file is valid and not corrupted

3. **Missing required field**
   ```
   Error processing record 1: Record missing required UID field
   ```
   → Record will be skipped, check XML structure

### Error Logging

Errors are printed to console. For each file:
- Total records found
- Successfully processed count
- Error count

## 🧪 Testing

Run the test script to validate the parser:

```bash
cd for_xml
python test_xml_parser.py
```

The test script will:
- Create a sample XML file with test data
- Test all extraction methods
- Validate CSV output
- Check special character handling

## 📖 Related Documentation

- **`tables.md`**: Complete table structure and field specifications
- **XML Structure**: See sample `SCI.xml` for WOS XML format
- **Original TXT Parser**: See parent directory for text-based parser

## 🔄 Migration from TXT Parser

This XML parser is a parallel implementation to the existing TXT parser:

- **TXT Parser**: Uses `|_` as separator, outputs to `paper_output_extra/`
- **XML Parser**: Uses `,` as separator, outputs to `xml_output/`

Both can coexist in the same project.

## 📞 Support

For issues or questions:
1. Check `tables.md` for field specifications
2. Verify XML file structure matches WOS format
3. Check console output for specific error messages

## 🎯 Future Enhancements

Potential improvements:
- [ ] Progress bar for large files
- [ ] Parallel processing for multiple files
- [ ] Database export option
- [ ] Data validation and statistics
- [ ] Incremental processing (skip already processed records)

## 📄 License

This project is part of the WOS Parser toolkit.
