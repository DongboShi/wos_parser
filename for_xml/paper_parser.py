from author_name import AuthorName
from paper_ref import PaperRef
from fu_manager import FUManager
from author_addr import AuthorAddrManager
from common_def import FilePathDef
from common_def import OUTPUT_FILE_SEPARATOR
from rp_author_manager import RPAuthorManager


def get_ut_by_dict_data(dict_data: dict):
    return dict_data["UT"].split(":")[1]

class PaperInfo:
    def __init__(self):
        self.ut_char = ""
        self.ref_list = list()
        self.authors = list()
        self.authors_addr_manager = AuthorAddrManager()
        self.item_type = ""
        self.year = ""
        self.venue = ""
        self.pub_year = ""
        self.volume = ""
        self.issue = ""
        self.first_pg = ""
        self.last_pg = ""
        self.pages = ""
        self.cite_count = ""
        self.cite_count_wide = ""
        self.lang = ""
        self.ref_count = ""
        self.TI = ""
        self.abstract = ""
        self.doi = ""
        self.SO = ""
        self.J9 = ""
        self.JI = ""
        self.SN = ""
        self.WC = ""
        self.fu_manager = FUManager()
        self.keywords_list = list()
        self.keywords_wide_list = list()
        self.field_list = list()
        self.field2_list = list()
        self.email_list = list()
        self.num_au = 0
        self.num_aff = 0
        self.num_country = 0
        self.rp_author_mng = RPAuthorManager()

    def load_by_ut_af(self, wos_af):
        author = wos_af.split(";")
        self.num_au = len(author)
        if self.num_au <= 0:
            print("wos_af: {}".format(wos_af))
        au_seq = 1
        for name in author:
            self.authors.append(AuthorName(name.strip(), au_seq))
            au_seq += 1
        pass

    def load_c1(self, c1):
        self.authors_addr_manager.load(c1)
        self.num_aff = self.authors_addr_manager.get_aff_num()
        self.num_country = self.authors_addr_manager.get_country_num()
        pass

    def load_ref(self, wos_cr):
        refs = wos_cr.split(";")
        for ref in refs:
            self.ref_list.append(PaperRef(ref.strip(), self.ut_char))
        pass

    def load_basic(self, data_dict):
        self.ut_char = get_ut_by_dict_data(data_dict)
        self.TI = data_dict["TI"]
        self.abstract = data_dict["AB"]
        self.SO = data_dict["SO"]
        self.J9 = data_dict["J9"]
        self.JI = data_dict["JI"]
        self.SN = data_dict["SN"]
        self.item_type = data_dict["DT"]
        self.volume = data_dict["VL"]
        self.pub_year = data_dict["PY"]
        self.issue = data_dict["IS"]
        self.first_pg = data_dict["BP"]
        self.last_pg = data_dict["EP"]
        self.pages = data_dict["PG"]
        self.cite_count = data_dict["TC"]
        self.cite_count_wide = data_dict["Z9"]
        self.lang = data_dict["LA"]
        self.doi = data_dict["DI"]
        self.ref_count = data_dict["NR"]

    def load_fu(self, fu):
        self.fu_manager.load(fu, self.ut_char)

    def load_keyword(self, keywords):
        de_split_arr = keywords.split(";")
        for de in de_split_arr:
            self.keywords_list.append(de.strip())

    def load_keyword_wide(self, ids):
        de_split_arr = ids.split(";")
        for de in de_split_arr:
            self.keywords_wide_list.append(de.strip())

    def load_field(self, sc):
        sc_list = sc.split(";")
        for sc in sc_list:
            self.field_list.append(sc.strip())

    def load_field2(self, wc):
        wc_list = wc.split(";")
        for wc in wc_list:  # type: str
            self.field2_list.append(wc.strip())

    def load_email(self, em):
        em_list = em.split(";")
        for em in em_list:
            self.email_list.append(em.strip())

    def load_rp(self, rp):
        self.rp_author_mng.load_rp_authors(rp)

    def load_by_data(self, data_dict):
        self.load_basic(data_dict)
        #self.load_fu(data_dict["FU"])
        #self.load_keyword(data_dict["DE"])
        #self.load_keyword_wide(data_dict["ID"])
        #self.load_field(data_dict["SC"])
        #self.load_field2(data_dict["WC"])
        #self.load_email(data_dict["EM"])
        self.load_by_ut_af(data_dict["AF"])
        #self.load_c1(data_dict["C1"])
        #self.load_ref(data_dict["CR"])
        self.load_rp(data_dict["RP"])
        pass

    def output_item(self):
        # ut_char, item_type, pub_year, volume, issue, first_pg, last_pg, pages, cite_count, cite_count_wide,
        # lang, doi, ref_count, num_country, num_au, num_aff, issn
        with open(FilePathDef.ITEM_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}{0}{9}{0}{10}{0}{11}{0}{12}{0}{13}{0}{14}{0}{15}{0}{16}{0}{17}\n"
                     .format(OUTPUT_FILE_SEPARATOR, self.ut_char, self.item_type, self.pub_year, self.volume, self.issue, self.first_pg
                     , self.last_pg, self.pages, self.cite_count, self.cite_count_wide, self.lang, self.doi
                     , self.ref_count, self.num_country, self.num_au, self.num_aff, self.SN))
        pass

    def output_item_author(self):
        with open(FilePathDef.ITEM_AUTHOR_FILE_PATH, 'a') as fs:
            for author in self.authors:     # type: AuthorName
                author.output_author(fs, self.ut_char)
            pass
        pass

    def output_item_title(self):
        # ut_char, ti
        with open(FilePathDef.ITEM_TITLE_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, self.TI))
        pass

    def output_item_abstract(self):
        # ut_char, abstract
        with open(FilePathDef.ITEM_ABSTRACT_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, self.abstract))

    def output_item_grant(self):
        # ut_char, grant, grant_code, grant_agency
        self.fu_manager.output_data(self.ut_char)

    def output_journal(self):
        # ut_char,SO,J9,JI,SN,pub_year
        with open(FilePathDef.ITEM_JOURNAL_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, self.SO, self.J9, self.JI, self.SN, self.pub_year))

    def output_keyword(self):
        # ut_char, keyword
        with open(FilePathDef.ITEM_KEYWORD_FILE_PATH, 'a') as fs:
            for keyword in self.keywords_list:
                fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, keyword))

    def output_keyword_wide(self):
        # ut_char, keyword_wide
        with open(FilePathDef.ITEM_KEYWORD_WIDE_FILE_PATH, 'a') as fs:
            for keyword in self.keywords_wide_list:
                fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, keyword))

    def output_email(self):
        # ut_char, email
        with open(FilePathDef.ITEM_EMAIL_FILE_PATH, 'a') as fs:
            for email in self.email_list:
                fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, email))

    def output_field(self):
        # ut_char, field
        with open(FilePathDef.ITEM_FIELD_FILE_PATH, 'a') as fs:
            for field in self.field_list:
                fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, field))

    def output_field2(self):
        # ut_char, field
        with open(FilePathDef.ITEM_FIELD2_FILE_PATH, 'a') as fs:
            for field in self.field2_list:
                fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.ut_char, field))

    def output_ref(self):
        for ref_inst in self.ref_list:      # type: PaperRef
            ref_inst.output(self.ut_char)

    def output_rp(self):
        self.rp_author_mng.output_rp_authors(self.ut_char)

    def output_data(self):
        #self.output_item()
        self.output_item_author()
        #self.output_item_title()
        #self.output_item_abstract()
        #self.output_item_grant()
        #self.output_journal()
        #self.output_keyword()
        #self.output_keyword_wide()
        #self.output_email()
        #self.output_field()
        #self.output_field2()
        #self.output_ref()
        #self.authors_addr_manager.output_item_au_addr(self.ut_char)
        self.output_rp()
        pass
