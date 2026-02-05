# Table Design for Extracting XML Data

This document outlines the table designs for structuring the data extracted from the XML files in the WOS Parser project.

------------------------------------------------------------------------

## 📝 1. Paper Basic Information Tables

### 1.1 item

This table contains the essential metadata of the papers.

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|----------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error or skip this record |
| sortdate | Publication date (from the `sortdate` attribute) | Yes | Raise an error |
| pubyear | Publication year (from the `pubyear` attribute) | Yes | Raise an error |
| has_abstract | Idicator of whether this record has abstract (from the `has_abstract` attribute) | Yes | Raise an error |
| vol | Journal volume (from the `vol` attribute) | No | Leave blank |
| issue | Journal issue (from the `issue` attribute) | No | Leave blank |
| part | Journal part (from the `part` attribute) | No | Leave blank |
| supplement | Supplement information (from the `supplement` attribute) | No | Leave blank |
| special_issue | Special issue information (from the `special_issue` attribute) | No | Leave blank |
| early_access_date | Early access date (from the `early_access_date` attribute ) | No | Leave blank |
| early_access_month | Early access month (from the `early_access_month` attribute ) | No | Leave blank |
| early_access_year | Early access year (from the `early_access_year` attribute ) | No | Leave blank |
| page_begin | First page (`<page>` tag `begin` attribute) | No | Leave blank |
| page_end | Last page (`<page>` tag `end` attribute) | No | Leave blank |
| page_count | Number of pages (`<page>` tag `count` attribute) | No | Leave blank |

------------------------------------------------------------------------

### 1.2 item_title

This table contains information about titles

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|---------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| title | Paper's main title (`<title type="item">` tag content) | Yes | Not every item has title, for which we could skip this table |

### 1.3 item_abstract

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|---------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| abstract | Abstract content (located in `<abstract_text>/<p>` tag) | Yes | Not every item has abstract, for which we could skip this table |

### 1.4 item_doc_types

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| doctype | Type of the record(`<doctype>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.5 item_doc_types_norm

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| doctype_norm | Normalized type of the record(`<normalized_doctypes>`/`<doctype>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.6 item_langs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| type | Type of the language (the `type` attribute of `language`) | Yes |  |
| language | Language of the record(`<language>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.7 item_langs_norm

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| type | Type of the language (the `type` attribute of `<normalized_languages>`/`<language>`) | Yes |  |
| language_norm | Language of the record(`<normalized_languages>`/`<language>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.8 item_editions

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| edition | Edition to which the record belongs (from the `edition` attribute) | Yes | Raise an error |

### 1.9 item_keywords

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| keyword | Keyword (from the `<keyword>` tag content) | Yes |  |

### 1.10 item_keywords_plus

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| keyword_plus | Keyword Plus (from the `<keyword_plus>/<keyword>` tag content) |  |  |

### 1.11 item_source

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| source | Source title (from the `<title type="source">` tag content) |  | Yes |
| source_abbrev | Abbreviated journal title (from the `<title type="source_abbrev">` tag content) | No | Leave blanck |
| abbrev_iso | ISO abbreviated journal title (from the `<title type="abbrev_iso">` tag content) | No | Leave blanck |
| abbrev_11 | 11-character abbreviated journal title (from the `<title type="abbrev_11">` tag content) | No | Leave blanck |
| abbrev_29 | 29-character abbreviated journal title (from the `<title type="abbrev_29">` tag content) | No | Leave blanck |
| series | Journal series (from the `<title type="series">` tag content) | No | Leave blanck |
| book_subtitle | Book subtitle (from the `<title type="book_subtitle">` tag content) | No | Leave blanck |

### 1.12 item_ids

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| identifier_type | Type of identifier (from the `type` attribute of `<identifier>` tag) | Yes |  |
| identifier_value | Identifier value (from the `value` attribute of `<identifier>` tag) | Yes |  |

### 1.13 item_oas

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| oa_type | Open access type (from the `type` attribute of `<oases>` tag) | Yes | Leave blank |

### 1.14 item_publishers

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| addr_no | Publisher address number (from the `addr_no` attribute of `<publisher>/<address_spec>` tag) | Yes | Leave blank |
| full_address | Full address text (from the `<publisher>/<address_spec>/<full_address>` tag content) | Yes | Leave blank |
| city | City (from the `<publisher>/<address_spec>/<city>` tag content) | | No | Leave blank |
| role | Publisher role (from the `role` attribute of `<name>` tag under `<publisher>`) | No | Leave blank |
| seq_no | Publisher sequence number (from the `seq_no` attribute of `<name>` tag under `<publisher>`) | No | Leave blank |
| display_name | Publisher display name (from the `<name>/<display_name>` tag content under `<publisher>`) | Yes | Leave blank |
| full_name | Publisher full name (from the `<name>/<full_name>` tag content under `<publisher>`) | Yes | Leave blank |
| unified_name | Publisher unified name (from the `<name>/<unified_name>` tag content under `<publisher>`) | No | Leave blank |

------------------------------------------------------------------------

## 👩‍💻 2. Author Information Tables

This table contains information about the authors of the papers.

### 2.1 item_authors

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`seq_no` attr) | Yes | Use default sequence |
| role | Author role (`role` attr) | No | Leave blank |
| reprint | Is reprint author (`reprint` attr) | No | Leave blank |
| display_name | Author's display name (`<display_name>`) | No | Leave blank |
| wos_standard | Author's WOS standard name (`<wos_standard>`) | No | Leave blank |
| full_name | Author's full name (`<full_name>`) | Yes | Raise an error or skip this record |
| first_name | Author's first name (`<first_name>`) | No | Leave blank |
| last_name | Author's last name (`<last_name>`) | No | Leave blank |
| suffix | Author's name suffix (`<suffix>`) | No | Leave blank |
| email_addr | Author’s email (`<email_addr>` tag) | No | Leave blank |

### 2.2 item_addresses

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| addr_no | Address number (`addr_no` attr) | Yes | Use default sequence |
| full_address | Full address text (`<full_address>` tag content) | Yes | Leave blank |
| city | City (`<city>` tag content) | No | Leave blank |
| state | State (`<state>` tag content) | No | Leave blank |
| country | Country (`<country>` tag content) | No | Leave blank |
| zip | Zip code (`<zip>` tag content) | No | Leave blank |
| zip_location | Zip location ( from `location` arttribute of `<zip>` tag) | No | Leave blank |

### 2.3 item_au_addrs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`<address_name>`/`<names, seq_no` attr) | Yes | Use default sequence |
| address_no | Author's address number (`<address_name>`/`<names,addr_no` attr) | No | Leave blank |

### 2.4 item_orgs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| addr_no | Address number (`addr_no` attr) | Yes | Use default sequence |
| org_pref | Organization prefix (`pref` attr) | Yes | Leave blank |
| ROR_ID | ROR identifier (`ROR_ID` attr) | No | Leave blank |
| org_id | Organization ID (`org_id` attr) | No | Leave blank |
| organization | Organization name (`<organization>` tag content) | Yes | Leave blank |

### 2.5 item_suborgs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| addr_no | Address number (`addr_no` attr) | Yes | Leave blank |
| suborganization | Suborganization (from `<suborganization>` tag content) | Yes | Leave blank |

### 2.6 item_author_ids

This table contains author identifiers. Information are obtained from `<names>` and `<addresses>` tags. 

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`<names>`/`seq_no` attr) | Yes | Use default sequence |
| r_id | ResearcherID (`r_id` attr from `<names>` tag) | No | Leave blank |
| orcid | ORCID identifier (`orcid_id` attr from `<names>` tag) | No | Leave blank |
| orcid_tr | ORCID trusted (`orcid_id_tr` attr from `<names>` tag) | No | Leave blank |

### 2.7 item_rp_addrs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| addr_no | Address number (`addr_no` attr under `<reprint_addresses>` tag) | Yes | Use default sequence |
| full_address | Full address text (`<full_address>` tag content under `<reprint_addresses>` tag) | Yes | Leave blank |
| city | City (`<city>` tag content under `<reprint_addresses>` tag) | No | Leave blank |
| state | State (`<state>` tag content under `<reprint_addresses>` tag) | No | Leave blank |
| country | Country (`<country>` tag content under `<reprint_addresses>` tag) | No | Leave blank |
| zip | Zip code (`<zip>` tag content under `<reprint_addresses>` tag ) | No | Leave blank |
| zip_location | Zip location ( from `location` arttribute of `<zip>` tag under `<reprint_addresses>` tag) | No | Leave blank |

### 2.8 item_rp_au_addrs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`<address_name>`/`<names, seq_no` attr under `<reprint_addresses>` tag) | Yes | Use default sequence |
| address_no | Author's address number (`<address_name>`/`<names,addr_no` attr under `<reprint_addresses>` tag) | No | Leave blank |

### 2.9 item_rp_orgs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| addr_no | Address number (`addr_no` attr under `<reprint_addresses>` tag) | Yes | Use default sequence |
| org_pref | Organization prefix (`pref` attr under `<reprint_addresses>` tag) | Yes | Leave blank |
| ROR_ID | ROR identifier (`ROR_ID` attr under `<reprint_addresses>` tag) | No | Leave blank |
| org_id | Organization ID (`org_id` attr under `<reprint_addresses>` tag) | No | Leave blank |
| organization | Organization name (`<organization>` tag content under `<reprint_addresses>` tag) | Yes | Leave blank |

### 2.10 item_rp_suborgs

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| addr_no | Address number (`addr_no` attr under `<reprint_addresses>` tag under `<reprint_addresses>` tag) | Yes | Leave blank |
| suborganization | Suborganization (from `<suborganization>` tag content under `<reprint_addresses>` tag) | Yes | Leave blank |

### 2.11 item_contributors

This table contains the names of authors for whom a Publons Profile/ResearcherID or an ORCID identifier is provided. Some authors have both IDs.

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`seq_no` attr) | Yes | Raise an error or skip this record |
| orcid_id | ORCID identifier (`orcid_id` attr) | No | Leave blank |
| r_id | ResearcherID (`r_id` attr) | No | Leave blank |
| r_id_role | ResearcherID role (`r_id_role` attr) | No | Leave blank |
| display_name | Author's display name (`<display_name>` tag content) | Yes | Leave blank |
| full_name | Author's full name (`<full_name>` tag content) | Yes | Raise an error or skip this record |
| first_name | Author's first name (`<first_name>` tag content) | No | Leave blank |
| last_name | Author's last name (`<last_name>` tag content) | No | Leave blank |

------------------------------------------------------------------------

## 🗂️ 3. Category Tables

This table contains information about the research fields associated with the papers.

### 3.1 item_headings
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| headings| Research field heading (from `<heading>` tag content) | Yes | Leave blank |

### 3.2 item_subjects
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| subject| Research subject (from `<subject>` tag content) | Yes | Leave blank |
| ascatype| ASCA type (from `ascatype` attribute of `<subject>` tag) | No | Leave blank |

------------------------------------------------------------------------

## 🔗 4. References Table

This table contains information about the references cited in the papers. Table 4.1 would be seperated into two tables, citations which contains citing-cited relationship within WOS and ref_patents which contains cited patents before loading into the database.

### 4.1 item_references

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| occurence_order | Order of the reference occurrence (from `occurrenceOrder` attribute of `<reference>` tag) | Yes | Raise an error or skip this record |
| cited_uid | Unique identifier for the cited paper (from `<uid>` content under `<reference>` tag) | No | Raise an error or skip this record |
| cited_author | Cited author name (from `<citedAuthor>` content under `<reference>` tag) | No | Leave blank |
| cited_year | Cited publication year (from `<Year>` content under `<reference>` tag) | No | Leave blank |
| cited_page | Cited page number (from `<page>` content under `<reference>` tag) | No | Leave blank |
| cited_volume | Cited volume number (from `<volume>` content under `<reference>` tag) | No | Leave blank |
| cited_title | Cited paper title (from `<citedTitle>` content under `<reference>` tag) | No | Leave blank |
| cited_work | Cited journal or book title (from `<citedWork>` content under `<reference>` tag) | No | Leave blank |
| cited_doi | Cited DOI (from `<doi>` content under `<reference>` tag) | No | Leave blank |
| cited_assignee | Cited patent assignee (from `<assignee>` content under `<reference>` tag) | No | Leave blank |
| patent_no | Cited patent number (from `<patent_no>` content under `<reference>` tag) | No | Leave blank |

### 4.2 item_cite_locations
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| occurence_order | Order of the reference occurrence (from `occurrenceOrder` attribute of `<reference>` tag) | Yes | Raise an error or skip this record |
| physical_location | Physical location of the citation (from `physicalLocation` attribute under `<reference>/<physicalSection>` tag) | No | Leave blank |
| section | Section of the citation (from `section` attribute under `<reference>/<physicalSection>` tag) | No | Leave blank |
| function | Function of the citation (from `function` attribute under `<reference>/<physicalSection>` tag) | No | Leave blank |

------------------------------------------------------------------------

## 💵 5. Funding Information Tables

### 5.1 item_acks

This table contains information on the acknowledgments related to the papers.

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| ack_text | Acknowledgment text (from `<ack_text>/<p>` tag content) | No | Leave blank |

### 5.2 item_grants
This table contains information on grants and funding related to the papers.

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| grant_agency | Grant agency name (from `<grant_agency>` tag content) | No | Leave blank |
| grant_agency_pref | Grant agency preferred name (from `pref` attribute of `<grant_agency>` tag) | No | Leave blank |
| grant_id | Grant ID (from `<grant_id>` tag content) | No | Leave blank |
| grant_source | Data source of the grant information (from `source` attribute of `<grant>` tag), default is WOS| No | Leave blank |

## 📢 6. Conference Information Table

This table contains information on conferences associated with the publications. This table would be seperated into two tables, item_conf_ids, and conference before loading into the database, to avoid redundancy.

### item_conferences

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| conf_id | Conference identifier (from `conf_id` attribute of `<conference>` tag) | Yes | Raise an error or skip this record |
| conf_info | Conference information (from `<conf_info>` tag content) | No | Leave blank |
| conf_title | Conference title (from `<conf_title>` tag content) | No | Leave blank |
| conf_start | Conference start date (from `conf_start` attribute of `<conf_date>` tag) | No | Leave blank |
| conf_end | Conference end date (from `conf_end` attribute of `<conf_date>` tag) | No | Leave blank |
| conf_date | Conference date text (from `<conf_date>` tag content) | No | Leave blank |
| conf_city | Conference city (from `<conf_city>` tag content) | No | Leave blank |
| conf_state | Conference state (from `<conf_state>` tag content) | No | Leave blank |
| sponsor | Conference sponsor (from `<sponsor>` tag content) | No | Leave blank |


------------------------------------------------------------------------

These table designs ensure structured and clean data extraction while providing flexibility for missing fields. The code will handle missing data using the predefined strategies specified in the "When Missing" column.