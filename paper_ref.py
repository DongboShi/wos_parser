import re
from enum import Enum
from common_def import FilePathDef
from common_def import OUTPUT_FILE_SEPARATOR

# VOLUME_PAGE_RE = re.compile(r'.*,[ ]*V(\d+),[ ]*P(\d+)(,.*|$)')
VOLUME_PAGE_RE = re.compile(r'.*,[ ]*V(\d+),[ ]*P(\d+).*')


class RefType(Enum):
    INVALID_REF = 0
    JOURNAL_REF = 1
    PATENT_REF = 2
    BOOK_REF = 3


class PaperRef:
    def __init__(self, ref, ut_char):
        self.ref = ref
        self.ref_type = None
        self.DOI = ""
        self.venue = ""
        self.volume = ""
        self.page = ""
        self.authors = None
        self.year = None

        if re.match(r'.*,.\d{4},.*,.V\d+,.P\d+.*', ref):
            self.ref_type = RefType.JOURNAL_REF
            ref_split_strs = ref.split(",")
            split_count = len(ref_split_strs)
            self.authors = ref_split_strs[0].strip()
            self.year = ref_split_strs[1].strip()
            result = VOLUME_PAGE_RE.search(ref)
            if result is None:
                print("ut {}, ref {}, volume invalid".format(ut_char, ref))
            result_groups = result.groups()
            self.volume = result_groups[0]
            if len(result_groups) > 1:
                self.page = result_groups[1]
            if ref.count("DOI "):
                self.DOI = re.sub(r'^DOI', '', ref_split_strs[-1].strip()).strip()
                # self.DOI = ref_split_strs[-1]
            if split_count >= 3:
                self.venue = ref_split_strs[2].strip()
            # if split_count >= 4:
            #     volume_str = re.findall(r'\d+', ref_split_strs[3])
            #     if len(volume_str) <= 0:
            #         print("ut {}, ref {}, volume not found in {}".format(ut_char, ref, ref_split_strs[3]))
            #     self.volume = volume_str[0].strip()
            # if split_count >= 5:
            #     self.page = re.findall(r'\d+', ref_split_strs[4])[0].strip()
        elif re.match(r'.*,.\d{4},.*Patent', ref):
            self.ref_type = RefType.PATENT_REF
            pass
        elif re.match(r'.*,.\d{4},.*', ref):
            self.ref_type = RefType.BOOK_REF
            pass

    def output_journal_ref(self, ut_char):
        # ut_char, authors, year, venue, volume, page
        with open(FilePathDef.ITEM_JOURNAL_REF_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}\n".format(OUTPUT_FILE_SEPARATOR,
                ut_char, self.ref, self.authors, self.year, self.venue, self.DOI, self.volume, self.page))
        pass

    def output_patent_ref(self, ut_char):
        # ut_char, ref
        with open(FilePathDef.ITEM_PATENT_REF_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, ut_char, self.ref))
        pass

    def output_book_ref(self, ut_char):
        # ut_char, ref
        with open(FilePathDef.ITEM_BOOK_REF_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, ut_char, self.ref))
        pass

    def output(self, ut_char):
        if self.ref_type == RefType.JOURNAL_REF:
            self.output_journal_ref(ut_char)
        elif self.ref_type == RefType.PATENT_REF:
            self.output_patent_ref(ut_char)
        elif self.ref_type == RefType.BOOK_REF:
            self.output_book_ref(ut_char)
        pass
