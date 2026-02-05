# Table Design for Extracting XML Data

This document outlines the table designs for structuring the data extracted from the XML files in the WOS Parser project.

------------------------------------------------------------------------

## 📝 1. Paper Basic Information Tables

### 1.1 item

This table contains the essential metadata of the papers.

| **Field Name** | **Description** | **Required** | **When Missing** |
|----------------|------------------------|----------------|----------------|
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

### 1.2 itemtitle

This table contains information about titles

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|-----------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error|
| title | Paper's main title (`<title type="item">` tag content) | Yes | Not every item has title, for which we could skip this table |

### 1.3 itemabstract

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|----------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error|
| abstract | Abstract content (located in `<abstract_text>/<p>` tag) | Yes | Not every item has abstract, for which we could skip this table |

### 1.4 itemdoctypes

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|---------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error|
| doctype | Type of the record(`<doctype>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.5 itemdoctypes_norm

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error|
| doctype_norm | Normalized type of the record(`<normalized_doctypes>`/`<doctype>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.6 itemlanguages

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| type | Type of the language (the `type` attribute of `language`) | Yes |  |
| language | Language of the record(`<language>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.7 itemlanguages_norm

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| type | Type of the language (the `type` attribute of `<normalized_languages>`/`<language>`) | Yes |  |
| language_norm | Language of the record(`<normalized_languages>`/`<language>` tag content) | Yes | Not every item has this value, for which we could skip this table |

### 1.8 itemeditions

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|---------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| edition | Edition to which the record belongs (from the `edition` attribute) | Yes | Raise an error  |

### 1.9 itemkeywords

| **Field Name** | **Description** | **Required** | **When Missing** |
|-----------------|---------------------|-----------------|-----------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| keyword | Keyword (from the `<keyword>` tag content) | Yes |  |

### 1.10 itemkeywords_plus
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| keyword_plus | Keyword Plus (from the `<keyword_plus>/<keyword>` tag content) |

### 1.11 itemsource
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| source | Source title (from the `<title type="source">` tag content) | | Yes | Leave blanck |
| source_abbrev | Abbreviated journal title (from the `<title type="source_abbrev">` tag content) | No | Leave blanck |
| abbrev_iso | ISO abbreviated journal title (from the `<title type="abbrev_iso">` tag content) | No | Leave blanck |
| abbrev_11 | 11-character abbreviated journal title (from the `<title type="abbrev_11">` tag content) | No | Leave blanck |
| abbrev_29 | 29-character abbreviated journal title (from the `<title type="abbrev_29">` tag content) | No | Leave blanck |
| series | Journal series (from the `<title type="series">` tag content) | No | Leave blanck |
| book_subtitle | Book subtitle (from the `<title type="book_subtitle">` tag content) | No | Leave blanck |

### 1.12 itemidentifiers
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| identifier_type | Type of identifier (from the `type` attribute of `<identifier>` tag) | Yes | |
| identifier_value | Identifier value (from the `value` attribute of `<identifier>` tag) | Yes | |

### 1.13 itemoas
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper (from `<UID>` tag) | Yes | Raise an error |
| oa_type | Open access type (from the `type` attribute of `<oases>` tag) | Yes | Leave blank |

------------------------------------------------------------------------

## 👩‍💻 2. Author Information Table

This table contains information about the authors of the papers.

### 2.1 itemauthors
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`seq_no` attr) | Yes | Use default sequence |
| role | Author role (`role` attr) | No | Leave blank |
| reprint | Is reprint author (`reprint` attr) | No | Leave blank |
| display_name | Author's display name (`<display_name>`) | No | Leave blank |
| wos_standard | Author's WOS standard name (`<wos_standard>`) | No | Leave blank |
| full_name | Author's full name (`<full_name>`) | Yes | Raise an error or skip this record |
| first_name | Author's first name (`<first_name>`) | No | Leave blank |
| last_name | Author's last name (`<last_name>`) | No | Leave blank |
| email_addr | Author’s email (`<email_addr>` tag) | No | Leave blank |


### 2.2 itemaddresses


### 2.3 itemauaddrs
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| uid | Unique identifier for the paper | Yes | Raise an error or skip this record |
| seq_no | Author sequence number (`seq_no` attr) | Yes | Use default sequence |
| address_no | Author's address number (`address_no` attr), list need to seperate by " " | No | Leave blank |

### 2.4 itemorganizations
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|

### 2.5 itemsuborgs
| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|

### 2.6 itemauthorids


------------------------------------------------------------------------

## 🔗 3. References Table

This table contains information about the references cited in the papers.

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|--------------------|------------------|------------------|
| UID | Unique identifier for the paper | Yes | Raise an error or skip this record |
| Ref_ID | Unique identifier for the reference | Yes | Fill with “Unknown” or leave blank |
| Cited Author | Cited author's name | No | Fill with "Unknown" |
| Cited Title | Cited article title | No | Fill with “Unknown” |
| Cited Work | Cited journal name | No | Fill with “Unknown” |
| Year | Year of the cited article | No | Fill with “Unknown” |
| Volume | Volume number of the cited article | No | Fill with “NA” |
| Page | Page number of the cited article | No | Fill with “NA” |
| DOI | Digital Object Identifier of the reference | No | Leave blank |

------------------------------------------------------------------------

## 💵 4. Funding Information Table

This table contains information on grants and funding related to the papers.

| **Field Name** | **Description** | **Required** | **When Missing** |
|------------------|-------------------|------------------|-------------------|
| UID | Unique identifier for the paper | Yes | Raise an error or skip this record |
| Grant Agency | Grant agency name | No | Fill with “Unknown” |
| Grant ID | Grant ID | No | Fill with “NA” |

------------------------------------------------------------------------

These table designs ensure structured and clean data extraction while providing flexibility for missing fields. The code will handle missing data using the predefined strategies specified in the "When Missing" column.