from author_name import AuthorName
from author_addr import AuthorAddrManager
from author_addr import AuthorAddrInfo
from common_def import FilePathDef
from common_def import OUTPUT_FILE_SEPARATOR
import re

RP_RE_PATTERN = re.compile(r'(.*?\(reprint author\).*?);')  # 重新修改正则表达式的逻辑，使用非贪婪的匹配方法
RP_CA_PATTERN = re.compile(r'(.*?\(corresponding author\).*?);')
RA_SPLIT_STR = "(reprint author)"
CA_SPLIT_STR = "(corresponding author)"
# RP_RE_PATTERN_BCK = re.compile(r'(.*\(reprint author\)[^;]*)[;]{0, 1}')   备用正则，上面的如果出问题了就用下面这个


class RPAuthorInfo:
    def __init__(self, rp_seq=1, name="", surname="", middle_name="", given_name="", addr="", country="", addr_md5=""):
        self.rp_seq = rp_seq
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.given_name = given_name
        self.addr = addr
        self.country = country
        self.addr_md5 = addr_md5

    def output_rp_author(self, fs, ut_char):
        if fs is None:
            return
        # rpseq, ut_char, name, surname, middlename, givenname, addr, country, addr_md5
        # fs.write("{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(self.rp_seq, ut_char, self.name, self.surname, self.middle_name
        #                                                , self.given_name, self.addr, self.country, self.addr_md5))
        fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}\n".format(OUTPUT_FILE_SEPARATOR, self.rp_seq, ut_char, self.name, self.surname
                                                       , self.given_name, self.addr, self.country, self.addr_md5))


class RPAuthorManager:
    def __init__(self):
        self.rp_list = list()

    def add_info_by_rp(self, rp_unit: str, rp_idx, split_pattern_str: str):
        name_split_str = rp_unit.split(split_pattern_str + ",")
        addr_split_str = rp_unit.split(split_pattern_str)

        add_count = 0

        author_addr = addr_split_str[1].strip()
        author_addr = author_addr.lstrip(',| ')
        author_addr = author_addr.rstrip('.')
        # print(rp_unit)
        # print(addr_split_str)
        # print(author_addr)
        au_addr_mng = AuthorAddrManager()
        au_addr_mng.load(author_addr)
        addr_tmp = au_addr_mng.get_first_addr()  # type: AuthorAddrInfo

        name_str = name_split_str[0].strip()
        name_spl = name_str.split(";")  # 当作者有两个名字时候，先行使用；拆分
        for name_sub in name_spl:
            rp_author = RPAuthorInfo()
            rp_author.rp_seq = rp_idx + add_count

            rp_author.name = name_sub
            author_name_info = AuthorName(rp_author.name, "")
            rp_author.surname = author_name_info.sur_name
            rp_author.middle_name = author_name_info.middle_name
            rp_author.given_name = author_name_info.given_name

            if len(addr_split_str) < 2:
                print("rp_unit: {}, split_str: {}".format(rp_unit, addr_split_str))
            rp_author.addr = author_addr
            rp_author.country = addr_tmp.country
            rp_author.addr_md5 = addr_tmp.addr_md5

            self.rp_list.append(rp_author)
            add_count += 1
        if add_count <= 0:
            print("rp add err: {}, idx {}, add_count {}".format(rp_unit, rp_idx, add_count))
            raise Exception("rp add err")
        return add_count

    def load_rp_authors_by_split_pattern(self, rp: str, split_pattern_str: str, re_pattern):
        is_succ = False
        if len(rp) <= 0:
            return is_succ
        rp_idx = 1
        # print(rp)
        rp_split_str = rp.split(split_pattern_str)
        rp_count = len(rp_split_str)
        if rp_count == 2:
            self.add_info_by_rp(rp, rp_idx, split_pattern_str)
            is_succ = True
        elif rp_count > 2:
            is_succ = True
            rp = rp + ";"  # 结尾增加一个；便于统一拆分
            complete_queue = re_pattern.findall(rp)
            for rp_unit in complete_queue:
                add_count = self.add_info_by_rp(rp_unit, rp_idx, split_pattern_str)
                rp_idx += add_count
        else:
            is_succ = False
        return is_succ

    def load_rp_authors(self, rp: str):
        is_succ = self.load_rp_authors_by_split_pattern(rp, RA_SPLIT_STR, RP_RE_PATTERN)
        if is_succ:
            return
        is_succ = self.load_rp_authors_by_split_pattern(rp, CA_SPLIT_STR, RP_CA_PATTERN)
        if not is_succ:
            print("rp invalid: {}".format(rp))

    def output_rp_authors(self, ut_char: str):
        with open(FilePathDef.RP_AUTHORS_FILE_PATH, 'a') as fs:
            for rp_unit in self.rp_list:        # type: RPAuthorInfo
                rp_unit.output_rp_author(fs, ut_char)
