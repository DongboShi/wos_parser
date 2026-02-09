"""
XML Record Parser for Web of Science Data

This module provides the core XMLRecordParser class that extracts data from
WOS XML records and structures it according to the table design in tables.md
"""  

import xml.etree.ElementTree as ET
from xml_common_def import WOS_NAMESPACE


class XMLRecordParser:
    """Parser for a single WOS XML record (<REC> element)"""
    
    def __init__(self, record_element):
        """
        Initialize parser with a record element
        
        :param record_element: XML Element representing a <REC> node
        """
        self.record = record_element
        self.ns = WOS_NAMESPACE
        self.uid = self._extract_uid()
        
    def _extract_uid(self):
        """Extract UID from record"""
        uid_elem = self.record.find('ns:UID', self.ns)
        if uid_elem is None:
            raise ValueError("Record missing required UID field")
        return uid_elem.text.strip()
    
    def _get_text(self, element, default=""):
        """Safely get text from an element"""
        if element is not None and element.text:
            return element.text.strip()
        return default
    
    def _get_attr(self, element, attr_name, default=""):
        """Safely get attribute from an element"""
        if element is not None:
            return element.attrib.get(attr_name, default)
        return default
    
    ==================================================================
    Section 1: Paper Basic Information Extraction
    ==================================================================
    
    def extract_item(self):
        """Extract data for item table (1.1)"""
        pub_info = self.record.find('.//ns:pub_info', self.ns)
        page = self.record.find('.//ns:pub_info/ns:page', self.ns)
        
        return {
            'uid': self.uid,
            'sortdate': self._get_attr(pub_info, 'sortdate'),
            'pubyear': self._get_attr(pub_info, 'pubyear'),
            'has_abstract': self._get_attr(pub_info, 'has_abstract'),
            'vol': self._get_attr(pub_info, 'vol'),
            'issue': self._get_attr(pub_info, 'issue'),
            'part': self._get_attr(pub_info, 'part'),
            'supplement': self._get_attr(pub_info, 'supplement'),
            'special_issue': self._get_attr(pub_info, 'special_issue'),
            'early_access_date': self._get_attr(pub_info, 'early_access_date'),
            'early_access_month': self._get_attr(pub_info, 'early_access_month'),
            'early_access_year': self._get_attr(pub_info, 'early_access_year'),
            'page_begin': self._get_attr(page, 'begin'),
            'page_end': self._get_attr(page, 'end'),
            'page_count': self._get_attr(page, 'page_count')
        }
    
    def extract_item_title(self):
        """Extract data for item_title table (1.2)"""
        title_elem = self.record.find('.//ns:title[@type="item"]', self.ns)
        if title_elem is None:
            return None  # Skip if no title
        
        return {
            'uid': self.uid,
            'title': self._get_text(title_elem)
        }
    
    def extract_item_abstract(self):
        """Extract data for item_abstract table (1.3)"""
        abstract_elem = self.record.find('.//ns:abstract_text/ns:p', self.ns)
        if abstract_elem is None:
            return None  # Skip if no abstract
        
        return {
            'uid': self.uid,
            'abstract': self._get_text(abstract_elem)
        }
    
    def extract_item_doc_types(self):
        """Extract data for item_doc_types table (1.4)"""
        doctypes = []
        for doctype in self.record.findall('.//ns:doctypes/ns:doctype', self.ns):
            doctypes.append({
                'uid': self.uid,
                'doctype': self._get_text(doctype)
            })
        return doctypes if doctypes else None
    
    def extract_item_doc_types_norm(self):
        """Extract data for item_doc_types_norm table (1.5)"""
        doctypes_norm = []
        for doctype in self.record.findall('.//ns:normalized_doctypes/ns:doctype', self.ns):
            doctypes_norm.append({
                'uid': self.uid,
                'doctype_norm': self._get_text(doctype)
            })
        return doctypes_norm if doctypes_norm else None
    
    def extract_item_langs(self):
        """Extract data for item_langs table (1.6)"""
        langs = []
        for lang in self.record.findall('.//ns:languages/ns:language', self.ns):
            langs.append({
                'uid': self.uid,
                'type': self._get_attr(lang, 'type'),
                'language': self._get_text(lang)
            })
        return langs if langs else None
    
    def extract_item_langs_norm(self):
        """Extract data for item_langs_norm table (1.7)"""
        langs_norm = []
        for lang in self.record.findall('.//ns:normalized_languages/ns:language', self.ns):
            langs_norm.append({
                'uid': self.uid,
                'type': self._get_attr(lang, 'type'),
                'language_norm': self._get_text(lang)
            })
        return langs_norm if langs_norm else None
    
    def extract_item_editions(self):
        """Extract data for item_editions table (1.8)"""
        editions = []
        for edition in self.record.findall('.//ns:EWUID/ns:edition', self.ns):
            editions.append({
                'uid': self.uid,
                'edition': self._get_attr(edition, 'value')
            })
        return editions if editions else None
    
    def extract_item_keywords(self):
        """Extract data for item_keywords table (1.9)"""
        keywords = []
        for keyword in self.record.findall('.//ns:keywords/ns:keyword', self.ns):
            keywords.append({
                'uid': self.uid,
                'keyword': self._get_text(keyword)
            })
        return keywords if keywords else None
    
    def extract_item_keywords_plus(self):
        """Extract data for item_keywords_plus table (1.10)"""
        keywords_plus = []
        for keyword in self.record.findall('.//ns:keywords_plus/ns:keyword', self.ns):
            keywords_plus.append({
                'uid': self.uid,
                'keyword_plus': self._get_text(keyword)
            })
        return keywords_plus if keywords_plus else None
    
    def extract_item_source(self):
        """Extract data for item_source table (1.11)"""
        return {
            'uid': self.uid,
            'source': self._get_text(self.record.find('.//ns:title[@type="source"]', self.ns)),
            'source_abbrev': self._get_text(self.record.find('.//ns:title[@type="source_abbrev"]', self.ns)),
            'abbrev_iso': self._get_text(self.record.find('.//ns:title[@type="abbrev_iso"]', self.ns)),
            'abbrev_11': self._get_text(self.record.find('.//ns:title[@type="abbrev_11"]', self.ns)),
            'abbrev_29': self._get_text(self.record.find('.//ns:title[@type="abbrev_29"]', self.ns)),
            'series': self._get_text(self.record.find('.//ns:title[@type="series"]', self.ns)),
            'book_subtitle': self._get_text(self.record.find('.//ns:title[@type="book_subtitle"]', self.ns))
        }
    
    def extract_item_ids(self):
        """Extract data for item_ids table (1.12)"""
        identifiers = []
        for identifier in self.record.findall('.//ns:identifiers/ns:identifier', self.ns):
            identifiers.append({
                'uid': self.uid,
                'identifier_type': self._get_attr(identifier, 'type'),
                'identifier_value': self._get_attr(identifier, 'value')
            })
        return identifiers if identifiers else None
    
    def extract_item_oas(self):
        """Extract data for item_oas table (1.13)"""
        oas_list = []
        for oa in self.record.findall('.//ns:oases/ns:oas', self.ns):
            oas_list.append({
                'uid': self.uid,
                'oa_type': self._get_attr(oa, 'type')
            })
        return oas_list if oas_list else None
    
    def extract_item_publishers(self):
        """Extract data for item_publishers table (1.14)"""
        publishers = []
        for publisher in self.record.findall('.//ns:publishers/ns:publisher', self.ns):
            addr_spec = publisher.find('ns:address_spec', self.ns)
            name_elem = publisher.find('.//ns:names/ns:name', self.ns)
            
            publishers.append({
                'uid': self.uid,
                'addr_no': self._get_attr(addr_spec, 'addr_no'),
                'full_address': self._get_text(addr_spec.find('ns:full_address', self.ns) if addr_spec else None),
                'city': self._get_text(addr_spec.find('ns:city', self.ns) if addr_spec else None),
                'role': self._get_attr(name_elem, 'role'),
                'seq_no': self._get_attr(name_elem, 'seq_no'),
                'display_name': self._get_text(name_elem.find('ns:display_name', self.ns) if name_elem else None),
                'full_name': self._get_text(name_elem.find('ns:full_name', self.ns) if name_elem else None),
                'unified_name': self._get_text(name_elem.find('ns:unified_name', self.ns) if name_elem else None)
            })
        return publishers if publishers else None
    
    ==================================================================
    Section 2: Author Information Extraction
    ==================================================================
    
    def extract_item_authors(self):
        """Extract data for item_authors table (2.1)"""
        authors = []
        for name in self.record.findall('.//ns:summary/ns:names/ns:name[@role="author"]', self.ns):
            authors.append({
                'uid': self.uid,
                'seq_no': self._get_attr(name, 'seq_no'),
                'role': self._get_attr(name, 'role'),
                'reprint': self._get_attr(name, 'reprint'),
                'display_name': self._get_text(name.find('ns:display_name', self.ns)),
                'wos_standard': self._get_text(name.find('ns:wos_standard', self.ns)),
                'full_name': self._get_text(name.find('ns:full_name', self.ns)),
                'first_name': self._get_text(name.find('ns:first_name', self.ns)),
                'last_name': self._get_text(name.find('ns:last_name', self.ns)),
                'suffix': self._get_text(name.find('ns:suffix', self.ns)),
                'email_addr': self._get_text(name.find('ns:email_addr', self.ns))
            })
        return authors if authors else None
    
    def extract_item_addresses(self):
        """Extract data for item_addresses table (2.2)"""
        addresses = []
        for addr_name in self.record.findall('.//ns:addresses/ns:address_name', self.ns):
            addr_spec = addr_name.find('ns:address_spec', self.ns)
            if addr_spec is not None:
                zip_elem = addr_spec.find('ns:zip', self.ns)
                addresses.append({
                    'uid': self.uid,
                    'addr_no': self._get_attr(addr_spec, 'addr_no'),
                    'full_address': self._get_text(addr_spec.find('ns:full_address', self.ns)),
                    'city': self._get_text(addr_spec.find('ns:city', self.ns)),
                    'state': self._get_text(addr_spec.find('ns:state', self.ns)),
                    'country': self._get_text(addr_spec.find('ns:country', self.ns)),
                    'zip': self._get_text(zip_elem),
                    'zip_location': self._get_attr(zip_elem, 'location')
                })
        return addresses if addresses else None
    
    def extract_item_addr_aus(self):
        """Extract data for item_addr_aus table (2.3)"""
        addr_aus = []
        for addr_name in self.record.findall('.//ns:addresses/ns:address_name', self.ns):
            for name in addr_name.findall('ns:names/ns:name', self.ns):
                addr_aus.append({
                    'uid': self.uid,
                    'seq_no': self._get_attr(name, 'seq_no'),
                    'address_no': self._get_attr(name, 'addr_no')
                })
        return addr_aus if addr_aus else None
    
    def extract_item_au_addrs(self):
        """Extract data for item_au_addrs table (2.4)"""
        au_addrs = []
        for name in self.record.findall('.//ns:summary/ns:names/ns:name[@role="author"]', self.ns):
            au_addrs.append({
                'uid': self.uid,
                'seq_no': self._get_attr(name, 'seq_no'),
                'address_no': self._get_attr(name, 'addr_no')
            })
        return au_addrs if au_addrs else None

    def extract_item_orgs(self):
        """Extract data for item_orgs table (2.4)"""
        orgs = []
        for addr_name in self.record.findall('.//ns:addresses/ns:address_name', self.ns):
            addr_spec = addr_name.find('ns:address_spec', self.ns)
            addr_no = self._get_attr(addr_spec, 'addr_no')
            
            for org in addr_spec.findall('.//ns:organizations/ns:organization', self.ns) if addr_spec else []:
                orgs.append({
                    'uid': self.uid,
                    'addr_no': addr_no,
                    'org_pref': self._get_attr(org, 'pref'),
                    'ROR_ID': self._get_attr(org, 'ROR_ID'),
                    'org_id': self._get_attr(org, 'org_id'),
                    'organization': self._get_text(org)
                })
        return orgs if orgs else None
    
    def extract_item_suborgs(self):
        """Extract data for item_suborgs table (2.5)"""
        suborgs = []
        for addr_name in self.record.findall('.//ns:addresses/ns:address_name', self.ns):
            addr_spec = addr_name.find('ns:address_spec', self.ns)
            addr_no = self._get_attr(addr_spec, 'addr_no')
            
            for suborg in addr_spec.findall('.//ns:suborganizations/ns:suborganization', self.ns) if addr_spec else []:
                suborgs.append({
                    'uid': self.uid,
                    'addr_no': addr_no,
                    'suborganization': self._get_text(suborg)
                })
        return suborgs if suborgs else None
    
    def extract_item_author_ids(self):
        """Extract data for item_author_ids table (2.6)"""
        author_ids = []
        for name in self.record.findall('.//ns:addresses/ns:address_name/ns:names/ns:name', self.ns):
            r_id = self._get_attr(name, 'r_id')
            orcid = self._get_attr(name, 'orcid_id')
            orcid_tr = self._get_attr(name, 'orcid_id_tr')
            
            if r_id or orcid or orcid_tr:  # Only add if at least one ID exists
                author_ids.append({
                    'uid': self.uid,
                    'seq_no': self._get_attr(name, 'seq_no'),
                    'r_id': r_id,
                    'orcid': orcid,
                    'orcid_tr': orcid_tr
                })
        return author_ids if author_ids else None
    
    def extract_item_rp_addrs(self):
        """Extract data for item_rp_addrs table (2.7)"""
        rp_addrs = []
        for addr_name in self.record.findall('.//ns:reprint_addresses/ns:address_name', self.ns):
            addr_spec = addr_name.find('ns:address_spec', self.ns)
            if addr_spec is not None:
                zip_elem = addr_spec.find('ns:zip', self.ns)
                rp_addrs.append({
                    'uid': self.uid,
                    'addr_no': self._get_attr(addr_spec, 'addr_no'),
                    'full_address': self._get_text(addr_spec.find('ns:full_address', self.ns)),
                    'city': self._get_text(addr_spec.find('ns:city', self.ns)),
                    'state': self._get_text(addr_spec.find('ns:state', self.ns)),
                    'country': self._get_text(addr_spec.find('ns:country', self.ns)),
                    'zip': self._get_text(zip_elem),
                    'zip_location': self._get_attr(zip_elem, 'location')
                })
        return rp_addrs if rp_addrs else None
    
    def extract_item_rp_au_addrs(self):
        """Extract data for item_rp_au_addrs table (2.8)"""
        rp_au_addrs = []
        for addr_name in self.record.findall('.//ns:reprint_addresses/ns:address_name', self.ns):
            for name in addr_name.findall('ns:names/ns:name', self.ns):
                rp_au_addrs.append({
                    'uid': self.uid,
                    'seq_no': self._get_attr(name, 'seq_no'),
                    'address_no': self._get_attr(name, 'addr_no')
                })
        return rp_au_addrs if rp_au_addrs else None
    
    def extract_item_rp_orgs(self):
        """Extract data for item_rp_orgs table (2.9)"""
        rp_orgs = []
        for addr_name in self.record.findall('.//ns:reprint_addresses/ns:address_name', self.ns):
            addr_spec = addr_name.find('ns:address_spec', self.ns)
            addr_no = self._get_attr(addr_spec, 'addr_no')
            
            for org in addr_spec.findall('.//ns:organizations/ns:organization', self.ns) if addr_spec else []:
                rp_orgs.append({
                    'uid': self.uid,
                    'addr_no': addr_no,
                    'org_pref': self._get_attr(org, 'pref'),
                    'ROR_ID': self._get_attr(org, 'ROR_ID'),
                    'org_id': self._get_attr(org, 'org_id'),
                    'organization': self._get_text(org)
                })
        return rp_orgs if rp_orgs else None
    
    def extract_item_rp_suborgs(self):
        """Extract data for item_rp_suborgs table (2.10)"""
        rp_suborgs = []
        for addr_name in self.record.findall('.//ns:reprint_addresses/ns:address_name', self.ns):
            addr_spec = addr_name.find('ns:address_spec', self.ns)
            addr_no = self._get_attr(addr_spec, 'addr_no')
            
            for suborg in addr_spec.findall('.//ns:suborganizations/ns:suborganization', self.ns) if addr_spec else []:
                rp_suborgs.append({
                    'uid': self.uid,
                    'addr_no': addr_no,
                    'suborganization': self._get_text(suborg)
                })
        return rp_suborgs if rp_suborgs else None
    
    def extract_item_contributors(self):
        """Extract data for item_contributors table (2.11)"""
        contributors = []
        for contributor in self.record.findall('.//ns:contributors/ns:contributor', self.ns):
            name = contributor.find('ns:name', self.ns)
            if name is not None:
                contributors.append({
                    'uid': self.uid,
                    'seq_no': self._get_attr(name, 'seq_no'),
                    'orcid_id': self._get_attr(name, 'orcid_id'),
                    'r_id': self._get_attr(name, 'r_id'),
                    'r_id_role': self._get_attr(name, 'role'),
                    'display_name': self._get_text(name.find('ns:display_name', self.ns)),
                    'full_name': self._get_text(name.find('ns:full_name', self.ns)),
                    'first_name': self._get_text(name.find('ns:first_name', self.ns)),
                    'last_name': self._get_text(name.find('ns:last_name', self.ns))
                })
        return contributors if contributors else None
    
    # ==================================================================
    # Section 3: Category Information Extraction
    # ==================================================================
    
    def extract_item_headings(self):
        """Extract data for item_headings table (3.1)"""
        headings = []
        for heading in self.record.findall('.//ns:category_info/ns:headings/ns:heading', self.ns):
            headings.append({
                'uid': self.uid,
                'headings': self._get_text(heading)
            })
        return headings if headings else None
    
    def extract_item_subjects(self):
        """Extract data for item_subjects table (3.2)"""
        subjects = []
        for subject in self.record.findall('.//ns:category_info/ns:subjects/ns:subject', self.ns):
            subjects.append({
                'uid': self.uid,
                'subject': self._get_text(subject),
                'ascatype': self._get_attr(subject, 'ascatype')
            })
        return subjects if subjects else None
    
    # ==================================================================
    # Section 4: References Extraction
    # ==================================================================
    
    def extract_item_references(self):
        """Extract data for item_references table (4.1)"""
        references = []
        for ref in self.record.findall('.//ns:references/ns:reference', self.ns):
            references.append({
                'uid': self.uid,
                'occurence_order': self._get_attr(ref, 'occurenceOrder'),
                'cited_uid': self._get_text(ref.find('ns:uid', self.ns)),
                'cited_author': self._get_text(ref.find('ns:citedAuthor', self.ns)),
                'cited_year': self._get_text(ref.find('ns:year', self.ns)),
                'cited_page': self._get_text(ref.find('ns:page', self.ns)),
                'cited_volume': self._get_text(ref.find('ns:volume', self.ns)),
                'cited_title': self._get_text(ref.find('ns:citedTitle', self.ns)),
                'cited_work': self._get_text(ref.find('ns:citedWork', self.ns)),
                'cited_doi': self._get_text(ref.find('ns:doi', self.ns)),
                'cited_assignee': self._get_text(ref.find('ns:assignee', self.ns)),
                'patent_no': self._get_text(ref.find('ns:patent_no', self.ns))
            })
        return references if references else None
    
    def extract_item_cite_locations(self):
        """Extract data for item_cite_locations table (4.2)"""
        cite_locations = []
        for ref in self.record.findall('.//ns:references/ns:reference', self.ns):
            occurence_order = self._get_attr(ref, 'occurenceOrder')
            
            for physical_section in ref.findall('ns:physicalSection', self.ns):
                cite_locations.append({
                    'uid': self.uid,
                    'occurence_order': occurence_order,
                    'physical_location': self._get_attr(physical_section, 'physicalLocation'),
                    'section': self._get_attr(physical_section, 'section'),
                    'function': self._get_attr(physical_section, 'function')
                })
        return cite_locations if cite_locations else None
    
    # ==================================================================
    # Section 5: Funding Information Extraction
    # ==================================================================
    
    def extract_item_acks(self):
        """Extract data for item_acks table (5.1)"""
        ack_elem = self.record.find('.//ns:fund_ack/ns:fund_text/ns:p', self.ns)
        if ack_elem is None:
            return None
        
        return {
            'uid': self.uid,
            'ack_text': self._get_text(ack_elem)
        }
    
    def extract_item_grants(self):
        """Extract data for item_grants table (5.2)"""
        grants = []
        for grant in self.record.findall('.//ns:fund_ack/ns:grants/ns:grant', self.ns):
            grant_agency_elem = grant.find('ns:grant_agency', self.ns)
            
            # Get all grant_agency elements (including preferred)
            grant_agencies = grant.findall('ns:grant_agency', self.ns)
            grant_agency = ""
            grant_agency_pref = ""
            
            for ga in grant_agencies:
                if self._get_attr(ga, 'pref') == 'Y':
                    grant_agency_pref = self._get_text(ga)
                elif not grant_agency:  # Get first non-preferred
                    grant_agency = self._get_text(ga)
            
            # Get all grant IDs
            for grant_id_elem in grant.findall('ns:grant_ids/ns:grant_id', self.ns):
                grants.append({
                    'uid': self.uid,
                    'grant_agency': grant_agency,
                    'grant_agency_pref': grant_agency_pref,
                    'grant_id': self._get_text(grant_id_elem),
                    'grant_source': self._get_attr(grant, 'source', 'WOS')
                })
        
        return grants if grants else None
    
    # ==================================================================
    # Section 6: Conference Information Extraction
    # ==================================================================
    
    def extract_item_conferences(self):
        """Extract data for item_conferences table (6)"""
        conferences = []
        for conf in self.record.findall('.//ns:conferences/ns:conference', self.ns):
            conf_date = conf.find('ns:conf_dates/ns:conf_date', self.ns)
            
            conferences.append({
                'uid': self.uid,
                'conf_id': self._get_attr(conf, 'conf_id'),
                'conf_info': self._get_text(conf.find('ns:conf_infos/ns:conf_info', self.ns)),
                'conf_title': self._get_text(conf.find('ns:conf_titles/ns:conf_title', self.ns)),
                'conf_start': self._get_attr(conf_date, 'conf_start'),
                'conf_end': self._get_attr(conf_date, 'conf_end'),
                'conf_date': self._get_text(conf_date),
                'conf_city': self._get_text(conf.find('ns:conf_locations/ns:conf_location/ns:conf_city', self.ns)),
                'conf_state': self._get_text(conf.find('ns:conf_locations/ns:conf_location/ns:conf_state', self.ns)),
                'sponsor': self._get_text(conf.find('ns:sponsors/ns:sponsor', self.ns))
            })
        
        return conferences if conferences else None