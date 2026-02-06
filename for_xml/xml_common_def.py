import os

# Output directory for XML parsed data
OUTPUT_DIR = "xml_output"

# Section 1: Paper Basic Information Tables
ITEM_FILE_NAME = "item.csv"
ITEM_TITLE_FILE_NAME = "item_title.csv"
ITEM_ABSTRACT_FILE_NAME = "item_abstract.csv"
ITEM_DOC_TYPES_FILE_NAME = "item_doc_types.csv"
ITEM_DOC_TYPES_NORM_FILE_NAME = "item_doc_types_norm.csv"
ITEM_LANGS_FILE_NAME = "item_langs.csv"
ITEM_LANGS_NORM_FILE_NAME = "item_langs_norm.csv"
ITEM_EDITIONS_FILE_NAME = "item_editions.csv"
ITEM_KEYWORDS_FILE_NAME = "item_keywords.csv"
ITEM_KEYWORDS_PLUS_FILE_NAME = "item_keywords_plus.csv"
ITEM_SOURCE_FILE_NAME = "item_source.csv"
ITEM_IDS_FILE_NAME = "item_ids.csv"
ITEM_OAS_FILE_NAME = "item_oas.csv"
ITEM_PUBLISHERS_FILE_NAME = "item_publishers.csv"

# Section 2: Author Information Tables
ITEM_AUTHORS_FILE_NAME = "item_authors.csv"
ITEM_ADDRESSES_FILE_NAME = "item_addresses.csv"
ITEM_AU_ADDRS_FILE_NAME = "item_au_addrs.csv"
ITEM_ADDR_AUS_FILE_NAME = "item_addr_aus.csv"
ITEM_ORGS_FILE_NAME = "item_orgs.csv"
ITEM_SUBORGS_FILE_NAME = "item_suborgs.csv"
ITEM_AUTHOR_IDS_FILE_NAME = "item_author_ids.csv"
ITEM_RP_ADDRS_FILE_NAME = "item_rp_addrs.csv"
ITEM_RP_AU_ADDRS_FILE_NAME = "item_rp_au_addrs.csv"
ITEM_RP_ORGS_FILE_NAME = "item_rp_orgs.csv"
ITEM_RP_SUBORGS_FILE_NAME = "item_rp_suborgs.csv"
ITEM_CONTRIBUTORS_FILE_NAME = "item_contributors.csv"

# Section 3: Category Tables
ITEM_HEADINGS_FILE_NAME = "item_headings.csv"
ITEM_SUBJECTS_FILE_NAME = "item_subjects.csv"

# Section 4: References Tables
ITEM_REFERENCES_FILE_NAME = "item_references.csv"
ITEM_CITE_LOCATIONS_FILE_NAME = "item_cite_locations.csv"

# Section 5: Funding Information Tables
ITEM_ACKS_FILE_NAME = "item_acks.csv"
ITEM_GRANTS_FILE_NAME = "item_grants.csv"

# Section 6: Conference Information Table
ITEM_CONFERENCES_FILE_NAME = "item_conferences.csv"


class XMLFilePathDef:
    """File paths for all CSV output files from XML parsing"""
    
    # Section 1: Paper Basic Information Tables
    ITEM_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_FILE_NAME)
    ITEM_TITLE_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_TITLE_FILE_NAME)
    ITEM_ABSTRACT_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_ABSTRACT_FILE_NAME)
    ITEM_DOC_TYPES_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_DOC_TYPES_FILE_NAME)
    ITEM_DOC_TYPES_NORM_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_DOC_TYPES_NORM_FILE_NAME)
    ITEM_LANGS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_LANGS_FILE_NAME)
    ITEM_LANGS_NORM_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_LANGS_NORM_FILE_NAME)
    ITEM_EDITIONS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_EDITIONS_FILE_NAME)
    ITEM_KEYWORDS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_KEYWORDS_FILE_NAME)
    ITEM_KEYWORDS_PLUS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_KEYWORDS_PLUS_FILE_NAME)
    ITEM_SOURCE_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_SOURCE_FILE_NAME)
    ITEM_IDS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_IDS_FILE_NAME)
    ITEM_OAS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_OAS_FILE_NAME)
    ITEM_PUBLISHERS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_PUBLISHERS_FILE_NAME)
    
    # Section 2: Author Information Tables
    ITEM_AUTHORS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_AUTHORS_FILE_NAME)
    ITEM_ADDRESSES_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_ADDRESSES_FILE_NAME)
    ITEM_AU_ADDRS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_AU_ADDRS_FILE_NAME)
    ITEM_ADDR_AUS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_ADDR_AUS_FILE_NAME)
    ITEM_SUBORGS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_SUBORGS_FILE_NAME)
    ITEM_AUTHOR_IDS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_AUTHOR_IDS_FILE_NAME)
    ITEM_RP_ADDRS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_RP_ADDRS_FILE_NAME)
    ITEM_RP_AU_ADDRS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_RP_AU_ADDRS_FILE_NAME)
    ITEM_RP_ORGS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_RP_ORGS_FILE_NAME)
    ITEM_RP_SUBORGS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_RP_SUBORGS_FILE_NAME)
    ITEM_CONTRIBUTORS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_CONTRIBUTORS_FILE_NAME)
    
    # Section 3: Category Tables
    ITEM_HEADINGS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_HEADINGS_FILE_NAME)
    ITEM_SUBJECTS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_SUBJECTS_FILE_NAME)
    
    # Section 4: References Tables
    ITEM_REFERENCES_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_REFERENCES_FILE_NAME)
    ITEM_CITE_LOCATIONS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_CITE_LOCATIONS_FILE_NAME)
    
    # Section 5: Funding Information Tables
    ITEM_ACKS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_ACKS_FILE_NAME)
    ITEM_GRANTS_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_GRANTS_FILE_NAME)
    
    # Section 6: Conference Information Table
    ITEM_CONFERENCES_FILE_PATH = os.path.join(OUTPUT_DIR, ITEM_CONFERENCES_FILE_NAME)


# XML Namespace definition for WOS XML files
WOS_NAMESPACE = {'ns': 'http://clarivate.com/schema/wok5.30/public/FullRecord'}
