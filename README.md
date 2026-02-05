# 🌟 WOS Parser

This repository contains the codebase for the WOS Parser, a data processing tool designed to handle and process Web of Science (WOS) data. This document outlines the relationships between the code components and explains the architecture of the project.

## Overview

The WOS Parser project is composed of several Python modules that work together to process large sets of WOS data, focusing on extracting and analyzing bibliographic information. The project is organized in a modular structure, ensuring scalability and clear separation of concerns.

┌───────────────────────────────────────────────────────────────────────────────┐
│                              WOS Parser System                                │
│                     (Dual-Mode Processing Architecture)                       │
└───────────────────────────────────────────────────────────────────────────────┘
                                       │
                       ┌───────────────┴────────────────┐
                       │                                │
        ┌──────────────▼─────────────┐    ┌─────────────▼────────────┐
        │      TXT Parser            │    │      XML Parser          │
        │    (Main Directory)        │    │    (for_xml/ dir)        │
        │                            │    │                          │
        │  Entry: parser_proc_main   │    │  Entry: xml_proc_main    │
        └──────────────┬─────────────┘    └─────────────┬────────────┘
                       │                                │
        ┌──────────────▼─────────────┐    ┌─────────────▼────────────┐
        │  paper_info_load_api       │    │  xml_info_load_api       │
        │  • load_paper_input()      │    │  • load_xml_file()       │
        │  • paper_info_proc()       │    │  • load_xml_directory()  │
        └──────────────┬─────────────┘    └─────────────┬────────────┘
                       │                                │
        ┌──────────────▼─────────────┐    ┌─────────────▼────────────┐
        │     Core Parser            │    │     Core Parser          │
        │                            │    │                          │
        │  ┌──────────────────────┐  │    │  ┌────────────────────┐  │
        │  │   paper_parser.py    │  │    │  │   xml_parser.py    │  │
        │  │   (PaperInfo class)  │  │    │  │ (XMLRecordParser)  │  │
        │  │                      │  │    │  │                    │  │
        │  │  Extracts:           │  │    │  │  Extracts:         │  │
        │  │  • Authors           │  │    │  │  • 33 CSV tables   │  │
        │  │  • Titles            │  │    │  │  • Authors         │  │
        │  │  • Abstracts         │  │    │  │  • References      │  │
        │  │  • Keywords          │  │    │  │  • Grants          │  │
        │  │  • References        │  │    │  │  • Addresses       │  │
        │  │  • Grants            │  │    │  └────────────────────┘  │
        │  └──────────┬───────────┘  │    └─────────────┬────────────┘
        │             │              │                  │
        │  ┌──────────▼───────────┐  │    ┌─────────────▼────────────┐
        │  │  Supporting Managers │  │    │    csv_writer.py         │
        │  │                      │  │    │  (XMLDataWriter class)   │
        │  │  • fu_manager        │  │    │                          │
        │  │    (Funding)         │  │    │  • write_record_data()   │
        │  │                      │  │    │  • write_item()          │
        │  │  • rp_author_manager │  │    │  • write_authors()       │
        │  │    (Reprint authors) │  │    │  • write_references()    │
        │  │                      │  │    │  • 33 write methods      │
        │  │  • author_addr       │  │    └─────────────┬────────────┘
        │  │    (Addresses)       │  │                  │
        │  │                      │  │    ┌─────────────▼────────────┐
        │  │  • txtparser         │  │    │ xml_processing_history   │
        │  │    (Text utilities)  │  │    │  (Incremental Proc)      │
        │  └──────────┬───────────┘  │    │                          │
        │             │              │    │  • Track processed UIDs  │
        │  ┌──────────▼───────────┐  │    │  • Skip duplicates       │
        │  │  proc_history_manager│  │    │  • Error logging         │
        │  │  • Track UTS         │  │    │  • Statistics            │
        │  │  • Avoid duplicates  │  │    └─────────────┬────────────┘
        │  └──────────┬───────────┘  │                  │
        │             │              │                  │
        │  ┌──────────▼───────────┐  │                  │
        │  │  filter_duplicate    │  │                  │
        │  │  • Deduplication     │  │                  │
        │  └──────────┬───────────┘  │                  │
        └─────────────┼──────────────┘                  │
                      │                                 │
        ┌─────────────▼─────────────┐    ┌──────────────▼───────────┐
        │  Output Files (TXT)       │    │  Output Files (XML)      │
        │                           │    │                          │
        │  Directory:               │    │  Directory:              │
        │    paper_output_extra/    │    │    xml_output/           │
        │                           │    │                          │
        │  Format:                  │    │  Format:                 │
        │    Separator: |_          │    │    Separator: , (comma)  │
        │                           │    │                          │
        │  Files:                   │    │  Files:                  │
        │  • item.txt               │    │  • item.csv              │
        │  • item_title.txt         │    │  • item_title.csv        │
        │  • item_authors.txt       │    │  • item_authors.csv      │
        │  • item_references.txt    │    │  • item_references.csv   │
        │  • item_grants.txt        │    │  • ... (33 CSV files)    │
        │  • ... (more files)       │    │                          │
        └───────────────────────────┘    └──────────────────────────┘

Common Configuration:
┌─────────────────────────────────────────────────────────────────────┐
│  common_def.py              │  xml_common_def.py                    │
│  • File paths               │  • XML namespaces                     │
│  • Output directories       │  • CSV file names (33 files)          │
│  • Constants                │  • Output directory                   │
└─────────────────────────────────────────────────────────────────────┘

The main modules and their roles include:

1. **parser_proc_main.py**: 
    Entry point of the application. This module initializes various components and orchestrates the data processing flow.

2. **paper_info_load_api.py**:
    Handles loading of WOS paper data from provided input files or directories and organizes the information into dictionaries. It also defines methods for temporary data processing.

3. **paper_parser.py**:
    Contains the main `PaperInfo` class, responsible for extracting and managing bibliographic metadata such as authors, title, abstracts, grants, keywords, and references. It interacts with various supporting managers.

4. **fu_manager.py**:
    Manages Funding (FU) information. This module defines a `FUManager` class to process, store, and output grant and funding-related information.

5. **state_code_analysis.py**:
    Loads and analyzes a list of U.S. state postal codes for validation purposes.

6. **rp_author_manager.py**:
    Manages reprint (RP) and corresponding author information. Provides mechanisms to load, process, and output reprint authors' information.

7. **common_def.py**:
    Defines constants and shared configurations used across the codebase. For example, output directories and file paths are centralized in this module.

8. **filter_dumplicate.py**:
    Identifies and removes duplicate entries from the input dataset.

9. **txtparser.py**:
    Contains helper functions for parsing and processing text-based WOS data.

## Code Relationships

Below is a description of how the different modules in the codebase interact with each other:

### `parser_proc_main.py`
This script acts as the main application entry point. It calls the following modules to perform data processing:
- **`state_code_analysis`**: Loads state postal codes using `load_state_code`.
- **`proc_history_manager`**: Loads historical Unique Topic Session (UTS) data using `load_history_uts`.
- **`paper_info_load_api`**: Manages paper input loading and processing using the `load_paper_input` and `paper_info_proc` methods.

### `paper_info_load_api.py`
This module loads input data and processes it using the provided callback function. It interacts with:
- **`parser_proc_main.py`**: Called to load data inputs.
- **`paper_parser.PaperInfo`**: A key class used for parsing and processing paper-specific metadata.
- **`proc_history_manager`**: Checks if UTs are already in processing history.

### `paper_parser.py`
The `PaperInfo` class in this module serves as the core of the application. It interacts with other classes and methods to load and parse data. It calls:
- **`fu_manager.FUManager.load_fu`**: Processes grants and funding information.
- **`rp_author_manager.RPAuthorManager.load_rp_authors`**: Processes reprint authors and assigns them to corresponding paper metadata.
- **`author_addr.AuthorAddrManager`**: Manages address-related information.
- It outputs major datasets to files (e.g., title, keywords) defined in `common_def.FilePathDef`.

### `fu_manager.py`
This module defines the `FUManager` and `FUInfo` classes to handle funding-related data for each paper. The methods include:
- Loading funding and grant information, parsing input data for each funding detail.
- Interacts with `paper_parser.PaperInfo` for grant processing and output.

### `rp_author_manager.py`
Defines the `RPAuthorManager` and `RPAuthorInfo` classes to manage reprint (RP) authors' metadata. Key methods:
- **`load_rp_authors`**: Loads authors using regular expression patterns defined in this module.
- **`output_rp_authors`**: Outputs processed authors' metadata into a file.

### `state_code_analysis.py`
Responsible for:
- Loading U.S. state postal codes from a CSV.
- Validating state codes using a lookup set.

### `common_def.py`
Acts as a shared configuration file. Defines file paths and formats for the output files.

### `filter_dumplicate.py`
- Utilizes `paper_info_load_api` for paper input processing.
- Ensures deduplication of input data based on unique identifiers like UT and Title.

### txtparser.py
Defines utility functions for extracting specific metadata from text inputs. Processes detailed attributes like publication year, citation counts, and abstracts.

## Key Data Flow
1. **Input**: The system takes WOS input data files or directories as the source.
    - `parser_proc_main.py` initializes the input process by calling methods from `paper_info_load_api.py`.
2. **Parsing**:
    - `paper_info_load_api.load_paper_input` parses input files to extract metadata into dictionaries.
    - Metadata is further processed by `PaperInfo` and its methods, e.g., `PaperInfo.load_fu`, `PaperInfo.load_rp`.
3. **Post-processing**:
    - Duplicate and invalid records are filtered by `filter_dumplicate.py`.
    - Address and author information is processed by `author_name`, `author_addr_manager`, and `rp_author_manager`.
    - Funding and grants are handled by `fu_manager.FUManager`.
4. **Output**:
    - Metadata such as abstracts, titles, authors, grants, and citations are outputted to files, with locations and formats defined in `common_def`.

---

## Installation

```bash
git clone https://github.com/DongboShi/wos_parser.git
cd wos_parser
pip install -r requirements.txt
```

## Usage

To run the WOS Parser, use the following command from the project directory:

```bash
python parser_proc_main.py
```

Make sure to place your input files in the corresponding `paper_input_src` directory.

---

## File Structure

```
wos_parser/
├── parser_proc_main.py       # Main entry point
├── paper_info_load_api.py    # Paper data loading and API definitions
├── filter_dumplicate.py      # Deduplication handling
├── paper_parser.py           # Core PaperInfo class for managing paper metadata
├── fu_manager.py             # Funding and grants management
├── rp_author_manager.py      # Reprint authors and corresponding authors management
├── state_code_analysis.py    # State code data loading and validation
├── txtparser.py              # Utility functions for text parsing
├── common_def.py             # Common constants and file path configurations
└── README.md                 # Documentation
```

## Authors
This project is maintained by [DongboShi](https://github.com/DongboShi).

---

## License

This repository is distributed under the terms of the MIT License. See the LICENSE file for more details.
