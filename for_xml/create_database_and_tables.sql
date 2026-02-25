-- =============================================================================
-- WOS XML Parser - Database and Table Creation Script
-- =============================================================================
-- This script creates the database schema for importing WOS XML Parser CSV output
-- into MySQL or MariaDB. It creates 33 tables organized into 6 sections.
--
-- Usage:
--   mysql -u root -p < create_database_and_tables.sql
--   OR
--   mariadb -u root -p < create_database_and_tables.sql
--
-- Note: You can customize the database name by replacing 'wos_xml' throughout
-- this file with your preferred database name.
-- =============================================================================

-- Create database (comment out if database already exists)
CREATE DATABASE IF NOT EXISTS wos_xml
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Use the database
USE wos_xml;

-- Temporarily disable foreign key checks for table creation
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================================
-- Section 1: Paper Basic Information Tables (14 tables)
-- =============================================================================

-- Main item table (must be created first as parent table)
CREATE TABLE IF NOT EXISTS item (
    uid VARCHAR(50),
    sortdate DATE,
    pubyear SMALLINT,
    has_abstract CHAR(1),
    vol VARCHAR(50),
    issue VARCHAR(50),
    part VARCHAR(50),
    supplement VARCHAR(200),
    special_issue VARCHAR(200),
    early_access_date VARCHAR(50),
    early_access_month VARCHAR(50),
    early_access_year VARCHAR(50),
    page_begin VARCHAR(20),
    page_end VARCHAR(20),
    page_count VARCHAR(20),
    INDEX pubyear (pubyear),
    INDEX uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paper titles
CREATE TABLE IF NOT EXISTS item_title (
    uid VARCHAR(50),
    title TEXT,
    INDEX idx_uid (uid),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paper abstracts with full-text search index
CREATE TABLE IF NOT EXISTS item_abstract (
    uid VARCHAR(50),
    abstract TEXT,
    INDEX idx_uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Document types
CREATE TABLE IF NOT EXISTS item_doc_types (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    doctype VARCHAR(100),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_doctype (doctype)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Normalized document types
CREATE TABLE IF NOT EXISTS item_doc_types_norm (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    doctype_norm VARCHAR(100),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_doctype_norm (doctype_norm)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Languages
CREATE TABLE IF NOT EXISTS item_langs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    type VARCHAR(50),
    language VARCHAR(100),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_language (language)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Normalized languages
CREATE TABLE IF NOT EXISTS item_langs_norm (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    type VARCHAR(50),
    language_norm VARCHAR(100),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_language_norm (language_norm)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- WOS editions
CREATE TABLE IF NOT EXISTS item_editions (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    edition VARCHAR(50),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_edition (edition)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Keywords
CREATE TABLE IF NOT EXISTS item_keywords (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    keyword VARCHAR(500),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_keyword (keyword(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Keywords Plus
CREATE TABLE IF NOT EXISTS item_keywords_plus (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    keyword_plus VARCHAR(500),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_keyword_plus (keyword_plus(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Source publication information
CREATE TABLE IF NOT EXISTS item_source (
    uid VARCHAR(50),
    source VARCHAR(500),
    source_abbrev VARCHAR(200),
    abbrev_iso VARCHAR(200),
    abbrev_11 VARCHAR(50),
    abbrev_29 VARCHAR(100),
    series VARCHAR(500),
    book_subtitle TEXT,
    UNIQUE INDEX idx_uid (uid),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_source (source(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Identifiers (DOI, ISSN, etc.)
CREATE TABLE IF NOT EXISTS item_ids (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    identifier_type VARCHAR(50),
    identifier_value VARCHAR(200),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_identifier_type (identifier_type),
    INDEX idx_identifier_value (identifier_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Open access information
CREATE TABLE IF NOT EXISTS item_oas (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    oa_type VARCHAR(100),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_oa_type (oa_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Publisher information
CREATE TABLE IF NOT EXISTS item_publishers (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    full_address TEXT,
    city VARCHAR(200),
    role VARCHAR(100),
    seq_no VARCHAR(50),
    display_name VARCHAR(500),
    full_name VARCHAR(500),
    unified_name VARCHAR(500),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- Section 2: Author Information Tables (12 tables)
-- =============================================================================

-- Author names and details
CREATE TABLE IF NOT EXISTS item_authors (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    seq_no VARCHAR(50),
    role VARCHAR(50),
    reprint CHAR(1),
    display_name VARCHAR(500),
    wos_standard VARCHAR(500),
    full_name VARCHAR(500),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    suffix VARCHAR(50),
    email_addr VARCHAR(200),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_full_name (full_name(255)),
    INDEX idx_last_name (last_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Author addresses
CREATE TABLE IF NOT EXISTS item_addresses (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    full_address TEXT,
    city VARCHAR(200),
    state VARCHAR(200),
    country VARCHAR(200),
    zip VARCHAR(50),
    zip_location VARCHAR(200),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_country (country),
    INDEX idx_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Author-address relationships
CREATE TABLE IF NOT EXISTS item_au_addrs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    seq_no VARCHAR(50),
    address_no VARCHAR(50),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_seq_no (seq_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Address-author relationships
CREATE TABLE IF NOT EXISTS item_addr_aus (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    seq_no VARCHAR(50),
    address_no VARCHAR(50),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_seq_no (seq_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Organizations
CREATE TABLE IF NOT EXISTS item_orgs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    org_pref VARCHAR(50),
    ROR_ID VARCHAR(100),
    org_id VARCHAR(100),
    organization VARCHAR(1000),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_organization (organization(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sub-organizations
CREATE TABLE IF NOT EXISTS item_suborgs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    suborganization VARCHAR(1000),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_suborganization (suborganization(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Author identifiers (ORCID, ResearcherID)
CREATE TABLE IF NOT EXISTS item_author_ids (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    seq_no VARCHAR(50),
    r_id VARCHAR(100),
    orcid VARCHAR(100),
    orcid_tr VARCHAR(100),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_orcid (orcid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reprint addresses
CREATE TABLE IF NOT EXISTS item_rp_addrs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    full_address TEXT,
    city VARCHAR(200),
    state VARCHAR(200),
    country VARCHAR(200),
    zip VARCHAR(50),
    zip_location VARCHAR(200),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_country (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reprint author-address relationships
CREATE TABLE IF NOT EXISTS item_rp_au_addrs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    seq_no VARCHAR(50),
    address_no VARCHAR(50),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reprint organizations
CREATE TABLE IF NOT EXISTS item_rp_orgs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    org_pref VARCHAR(50),
    ROR_ID VARCHAR(100),
    org_id VARCHAR(100),
    organization VARCHAR(1000),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_organization (organization(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reprint sub-organizations
CREATE TABLE IF NOT EXISTS item_rp_suborgs (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    addr_no VARCHAR(50),
    suborganization VARCHAR(1000),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contributors with IDs
CREATE TABLE IF NOT EXISTS item_contributors (
    id INT AUTO_INCREMENT,
    uid VARCHAR(50),
    seq_no VARCHAR(50),
    orcid_id VARCHAR(100),
    r_id VARCHAR(100),
    r_id_role VARCHAR(100),
    display_name VARCHAR(500),
    full_name VARCHAR(500),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    UNIQUE INDEX idx_id (id),
    FOREIGN KEY (uid) REFERENCES item(uid) ON DELETE CASCADE,
    INDEX idx_uid (uid),
    INDEX idx_orcid_id (orcid_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- Section 3: Category Information Tables (2 tables)
-- =============================================================================

-- Research headings
CREATE TABLE IF NOT EXISTS item_headings (
    uid VARCHAR(50),
    headings VARCHAR(500),
    INDEX idx_uid (uid),
    INDEX idx_headings (headings)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Research subjects
CREATE TABLE IF NOT EXISTS item_subjects (
    uid VARCHAR(50),
    subject VARCHAR(500),
    ascatype VARCHAR(50),
    INDEX idx_uid (uid),
    INDEX idx_subject (subject(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- Section 4: References Tables (2 tables)
-- =============================================================================

-- Cited references
CREATE TABLE IF NOT EXISTS item_references (
    uid VARCHAR(50),
    occurence_order VARCHAR(50),
    cited_uid VARCHAR(50),
    cited_author TEXT,
    cited_year VARCHAR(100),
    cited_page VARCHAR(1000),
    cited_volume VARCHAR(1000),
    cited_title TEXT,
    cited_work TEXT,
    cited_doi VARCHAR(500), 
    cited_assignee VARCHAR(500),
    patent_no VARCHAR(200),
    INDEX idx_uid (uid),
    INDEX idx_cited_uid (cited_uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Citation locations in text
CREATE TABLE IF NOT EXISTS item_cite_locations (
    uid VARCHAR(50),
    occurence_order VARCHAR(50),
    physical_location VARCHAR(200),
    section VARCHAR(200),
    function VARCHAR(200),
    INDEX idx_uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- Section 5: Funding Information Tables (2 tables)
-- =============================================================================

-- Acknowledgments with full-text search index
CREATE TABLE IF NOT EXISTS item_acks (
    uid VARCHAR(50),
    ack_text TEXT,
    INDEX idx_uid (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Grant information
CREATE TABLE IF NOT EXISTS item_grants (
    uid VARCHAR(50),
    grant_agency VARCHAR(1000),
    grant_agency_pref VARCHAR(500),
    grant_id VARCHAR(1000),
    grant_source VARCHAR(100),
    INDEX idx_uid (uid),
    INDEX idx_grant_agency (grant_agency),
    INDEX idx_grant_id (grant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- Section 6: Conference Information Table (1 table)
-- =============================================================================

-- Conference details
CREATE TABLE IF NOT EXISTS item_conferences (
    uid VARCHAR(50),
    conf_id VARCHAR(100),
    conf_info TEXT,
    conf_title VARCHAR(1000),
    conf_start VARCHAR(50),
    conf_end VARCHAR(50),
    conf_date VARCHAR(200),
    conf_city VARCHAR(200),
    conf_state VARCHAR(200),
    sponsor TEXT,
    INDEX idx_uid (uid),
    INDEX idx_conf_id (conf_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE citations AS SELECT uid, cited_uid FROM item_references WHERE cited_uid LIKE 'WOS:%';

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- End of schema creation
-- =============================================================================
