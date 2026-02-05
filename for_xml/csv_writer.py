"""
CSV Writer with proper escaping for WOS XML data

This module provides utilities to write data to CSV files with proper handling
of special characters like commas, quotes, and newlines.
"""

import csv
import os


class CSVWriter:
    """Handles writing data to CSV files with proper escaping"""
    
    def __init__(self, file_path, headers, mode='a'):
        """
        Initialize CSV writer
        
        :param file_path: Path to the CSV file
        :param headers: List of column headers
        :param mode: File mode ('w' for write, 'a' for append)
        """
        self.file_path = file_path
        self.headers = headers
        self.mode = mode
        self._ensure_dir()
        self._init_file()
    
    def _ensure_dir(self):
        """Ensure output directory exists"""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    def _init_file(self):
        """Initialize file with headers if writing new file"""
        if self.mode == 'w' or not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
    
    def write_row(self, data):
        """
        Write a single row to CSV
        
        :param data: Dictionary containing row data
        """
        if data is None:
            return
        
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(data)
    
    def write_rows(self, data_list):
        """
        Write multiple rows to CSV
        
        :param data_list: List of dictionaries containing row data
        """
        if not data_list:
            return
        
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerows(data_list)


class XMLDataWriter:
    """Manages all CSV writers for XML data extraction"""
    
    def __init__(self):
        """Initialize all CSV writers with their respective headers"""
        from xml_common_def import XMLFilePathDef
        
        # Section 1: Paper Basic Information
        self.item_writer = CSVWriter(
            XMLFilePathDef.ITEM_FILE_PATH,
            ['uid', 'sortdate', 'pubyear', 'has_abstract', 'vol', 'issue', 
             'part', 'supplement', 'special_issue', 'early_access_date', 
             'early_access_month', 'early_access_year', 'page_begin', 
             'page_end', 'page_count']
        )
        
        self.item_title_writer = CSVWriter(
            XMLFilePathDef.ITEM_TITLE_FILE_PATH,
            ['uid', 'title']
        )
        
        self.item_abstract_writer = CSVWriter(
            XMLFilePathDef.ITEM_ABSTRACT_FILE_PATH,
            ['uid', 'abstract']
        )
        
        self.item_doc_types_writer = CSVWriter(
            XMLFilePathDef.ITEM_DOC_TYPES_FILE_PATH,
            ['uid', 'doctype']
        )
        
        self.item_doc_types_norm_writer = CSVWriter(
            XMLFilePathDef.ITEM_DOC_TYPES_NORM_FILE_PATH,
            ['uid', 'doctype_norm']
        )
        
        self.item_langs_writer = CSVWriter(
            XMLFilePathDef.ITEM_LANGS_FILE_PATH,
            ['uid', 'type', 'language']
        )
        
        self.item_langs_norm_writer = CSVWriter(
            XMLFilePathDef.ITEM_LANGS_NORM_FILE_PATH,
            ['uid', 'type', 'language_norm']
        )
        
        self.item_editions_writer = CSVWriter(
            XMLFilePathDef.ITEM_EDITIONS_FILE_PATH,
            ['uid', 'edition']
        )
        
        self.item_keywords_writer = CSVWriter(
            XMLFilePathDef.ITEM_KEYWORDS_FILE_PATH,
            ['uid', 'keyword']
        )
        
        self.item_keywords_plus_writer = CSVWriter(
            XMLFilePathDef.ITEM_KEYWORDS_PLUS_FILE_PATH,
            ['uid', 'keyword_plus']
        )
        
        self.item_source_writer = CSVWriter(
            XMLFilePathDef.ITEM_SOURCE_FILE_PATH,
            ['uid', 'source', 'source_abbrev', 'abbrev_iso', 'abbrev_11', 
             'abbrev_29', 'series', 'book_subtitle']
        )
        
        self.item_ids_writer = CSVWriter(
            XMLFilePathDef.ITEM_IDS_FILE_PATH,
            ['uid', 'identifier_type', 'identifier_value']
        )
        
        self.item_oas_writer = CSVWriter(
            XMLFilePathDef.ITEM_OAS_FILE_PATH,
            ['uid', 'oa_type']
        )
        
        self.item_publishers_writer = CSVWriter(
            XMLFilePathDef.ITEM_PUBLISHERS_FILE_PATH,
            ['uid', 'addr_no', 'full_address', 'city', 'role', 'seq_no', 
             'display_name', 'full_name', 'unified_name']
        )
        
        # Section 2: Author Information
        self.item_authors_writer = CSVWriter(
            XMLFilePathDef.ITEM_AUTHORS_FILE_PATH,
            ['uid', 'seq_no', 'role', 'reprint', 'display_name', 
             'wos_standard', 'full_name', 'first_name', 'last_name', 
             'suffix', 'email_addr']
        )
        
        self.item_addresses_writer = CSVWriter(
            XMLFilePathDef.ITEM_ADDRESSES_FILE_PATH,
            ['uid', 'addr_no', 'full_address', 'city', 'state', 'country', 
             'zip', 'zip_location']
        )
        
        self.item_au_addrs_writer = CSVWriter(
            XMLFilePathDef.ITEM_AU_ADDRS_FILE_PATH,
            ['uid', 'seq_no', 'address_no']
        )
        
        self.item_orgs_writer = CSVWriter(
            XMLFilePathDef.ITEM_ORGS_FILE_PATH,
            ['uid', 'addr_no', 'org_pref', 'ROR_ID', 'org_id', 'organization']
        )
        
        self.item_suborgs_writer = CSVWriter(
            XMLFilePathDef.ITEM_SUBORGS_FILE_PATH,
            ['uid', 'addr_no', 'suborganization']
        )
        
        self.item_author_ids_writer = CSVWriter(
            XMLFilePathDef.ITEM_AUTHOR_IDS_FILE_PATH,
            ['uid', 'seq_no', 'r_id', 'orcid', 'orcid_tr']
        )
        
        self.item_rp_addrs_writer = CSVWriter(
            XMLFilePathDef.ITEM_RP_ADDRS_FILE_PATH,
            ['uid', 'addr_no', 'full_address', 'city', 'state', 'country', 
             'zip', 'zip_location']
        )
        
        self.item_rp_au_addrs_writer = CSVWriter(
            XMLFilePathDef.ITEM_RP_AU_ADDRS_FILE_PATH,
            ['uid', 'seq_no', 'address_no']
        )
        
        self.item_rp_orgs_writer = CSVWriter(
            XMLFilePathDef.ITEM_RP_ORGS_FILE_PATH,
            ['uid', 'addr_no', 'org_pref', 'ROR_ID', 'org_id', 'organization']
        )
        
        self.item_rp_suborgs_writer = CSVWriter(
            XMLFilePathDef.ITEM_RP_SUBORGS_FILE_PATH,
            ['uid', 'addr_no', 'suborganization']
        )
        
        self.item_contributors_writer = CSVWriter(
            XMLFilePathDef.ITEM_CONTRIBUTORS_FILE_PATH,
            ['uid', 'seq_no', 'orcid_id', 'r_id', 'r_id_role', 
             'display_name', 'full_name', 'first_name', 'last_name']
        )
        
        # Section 3: Category Information
        self.item_headings_writer = CSVWriter(
            XMLFilePathDef.ITEM_HEADINGS_FILE_PATH,
            ['uid', 'headings']
        )
        
        self.item_subjects_writer = CSVWriter(
            XMLFilePathDef.ITEM_SUBJECTS_FILE_PATH,
            ['uid', 'subject', 'ascatype']
        )
        
        # Section 4: References
        self.item_references_writer = CSVWriter(
            XMLFilePathDef.ITEM_REFERENCES_FILE_PATH,
            ['uid', 'occurence_order', 'cited_uid', 'cited_author', 
             'cited_year', 'cited_page', 'cited_volume', 'cited_title', 
             'cited_work', 'cited_doi', 'cited_assignee', 'patent_no']
        )
        
        self.item_cite_locations_writer = CSVWriter(
            XMLFilePathDef.ITEM_CITE_LOCATIONS_FILE_PATH,
            ['uid', 'occurence_order', 'physical_location', 'section', 'function']
        )
        
        # Section 5: Funding Information
        self.item_acks_writer = CSVWriter(
            XMLFilePathDef.ITEM_ACKS_FILE_PATH,
            ['uid', 'ack_text']
        )
        
        self.item_grants_writer = CSVWriter(
            XMLFilePathDef.ITEM_GRANTS_FILE_PATH,
            ['uid', 'grant_agency', 'grant_agency_pref', 'grant_id', 'grant_source']
        )
        
        # Section 6: Conference Information
        self.item_conferences_writer = CSVWriter(
            XMLFilePathDef.ITEM_CONFERENCES_FILE_PATH,
            ['uid', 'conf_id', 'conf_info', 'conf_title', 'conf_start', 
             'conf_end', 'conf_date', 'conf_city', 'conf_state', 'sponsor']
        )
    
    def write_record_data(self, parser):
        """
        Write all extracted data from a parsed record to CSV files
        
        :param parser: XMLRecordParser instance with extracted data
        """
        # Section 1: Paper Basic Information
        self.item_writer.write_row(parser.extract_item())
        self.item_title_writer.write_row(parser.extract_item_title())
        self.item_abstract_writer.write_row(parser.extract_item_abstract())
        self.item_doc_types_writer.write_rows(parser.extract_item_doc_types())
        self.item_doc_types_norm_writer.write_rows(parser.extract_item_doc_types_norm())
        self.item_langs_writer.write_rows(parser.extract_item_langs())
        self.item_langs_norm_writer.write_rows(parser.extract_item_langs_norm())
        self.item_editions_writer.write_rows(parser.extract_item_editions())
        self.item_keywords_writer.write_rows(parser.extract_item_keywords())
        self.item_keywords_plus_writer.write_rows(parser.extract_item_keywords_plus())
        self.item_source_writer.write_row(parser.extract_item_source())
        self.item_ids_writer.write_rows(parser.extract_item_ids())
        self.item_oas_writer.write_rows(parser.extract_item_oas())
        self.item_publishers_writer.write_rows(parser.extract_item_publishers())
        
        # Section 2: Author Information
        self.item_authors_writer.write_rows(parser.extract_item_authors())
        self.item_addresses_writer.write_rows(parser.extract_item_addresses())
        self.item_au_addrs_writer.write_rows(parser.extract_item_au_addrs())
        self.item_orgs_writer.write_rows(parser.extract_item_orgs())
        self.item_suborgs_writer.write_rows(parser.extract_item_suborgs())
        self.item_author_ids_writer.write_rows(parser.extract_item_author_ids())
        self.item_rp_addrs_writer.write_rows(parser.extract_item_rp_addrs())
        self.item_rp_au_addrs_writer.write_rows(parser.extract_item_rp_au_addrs())
        self.item_rp_orgs_writer.write_rows(parser.extract_item_rp_orgs())
        self.item_rp_suborgs_writer.write_rows(parser.extract_item_rp_suborgs())
        self.item_contributors_writer.write_rows(parser.extract_item_contributors())
        
        # Section 3: Category Information
        self.item_headings_writer.write_rows(parser.extract_item_headings())
        self.item_subjects_writer.write_rows(parser.extract_item_subjects())
        
        # Section 4: References
        self.item_references_writer.write_rows(parser.extract_item_references())
        self.item_cite_locations_writer.write_rows(parser.extract_item_cite_locations())
        
        # Section 5: Funding Information
        self.item_acks_writer.write_row(parser.extract_item_acks())
        self.item_grants_writer.write_rows(parser.extract_item_grants())
        
        # Section 6: Conference Information
        self.item_conferences_writer.write_rows(parser.extract_item_conferences())