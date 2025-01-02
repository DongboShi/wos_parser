import re
import hashlib
from addr_manager import make_addr_by_country
from common_def import FilePathDef
from common_def import OUTPUT_FILE_SEPARATOR


class AuthorAddrInfo:
    def __init__(self, au, addr, country, au_grp_seq, addr_md5):
        self.au = au
        self.addr = addr
        self.country = country
        self.au_grp_seq = au_grp_seq
        self.addr_md5 = addr_md5
        self.addr_info = None

    def addr_analysis(self):
        self.addr_info = make_addr_by_country(self.country, self.addr)
        pass

    def output_au_addr(self, fs, ut_char):
        # ut_char, augrpseq, addr, country, addr_md5
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n".format(OUTPUT_FILE_SEPARATOR, ut_char, self.au, self.au_grp_seq, self.addr, self.country, self.addr_md5))


class AuthorAddrManager:
    def __init__(self):
        self.author_addr_list = list()

    def load(self, c1: str):
        if c1 is None or len(c1) <= 0:
            return
        # 解决存在[wang,[liu]]这种格式数据的问题，删除中嵌套的[]
        if re.findall(r"\[[^(\[)]+?\[[^(\[)]+?\][^(\[)]*?\]", c1):
            iterc1 = re.finditer(r"\[[^(\[)]+?\[[^(\[)]+?\][^(\[)]*?\]", c1)
            for p in iterc1:
                old = p.group()
                pt = re.findall(r"\[[^(\[)]+?\]", old)[0]
                npt = re.sub('(\[)|(\])', '', pt)
                new = old.replace(pt, npt)
                c1 = c1.replace(old, new)
        if "[" in c1:
            complete_queue = re.split(r"\[", c1)
            complete_queue.pop(0)
            augrpseq = 1
            for i, p in enumerate(complete_queue, start=1):
                if "]" in p:
                    au = re.split(r"\]", p)[0]
                    authors = au.split(";")
                    address = re.split(r"\]", p)[1]
                    # addr = re.findall(r"\[([\s\S]+?)\]\s*([\s\S]+?)(?:;|$)", p)[0]
                    addrs = address.strip().split(";")
                    addrs = list(filter(None, addrs))
                    for addr in addrs:
                        if len(addr) <= 0:
                            continue
                        for author in authors:
                            if len(author) <= 0:
                                continue
                            # print("author: {}, address: {}, addr: {}".format(author, address, addr))
                            addr = re.sub(';', '', addr).strip()
                            addr = re.sub('|', '', addr)
                            # print("addr_sub_proc: {}".format(addr))
                            author = author.strip()
                            country = addr.split(",")[-1].strip()
                            addr_md5 = hashlib.md5()
                            addr_md5.update(addr.encode(encoding="utf-8"))
                            addrs_md5 = addr_md5.hexdigest()
                            if country.endswith("USA"):
                                country = "USA"

                            self.author_addr_list.append(AuthorAddrInfo(author, addr, country, augrpseq, addrs_md5))
                        augrpseq = augrpseq + 1
                else:
                    self.author_addr_list.append(AuthorAddrInfo(p, "", "", augrpseq, ""))
        else:
            addrs = c1.split("; ")
            for i, addr in enumerate(addrs, start=1):
                # print("i: {}, addr: {}".format(i, addr))
                addr = re.sub(';', '', addr).strip()
                addr = re.sub('|', '', addr)
                addr_md5 = hashlib.md5()
                addr_md5.update(addr.encode(encoding="utf-8"))
                addrs_md5 = addr_md5.hexdigest()
                country = addr.split(",")[-1].strip()
                if country.endswith("USA"):
                    country = "USA"
                self.author_addr_list.append(AuthorAddrInfo("", addr, country, i, addrs_md5))
        for addr_inst in self.author_addr_list:         # type: AuthorAddrInfo
            addr_inst.addr_analysis()

    # def country_load(self):
    #     for author_addr in self.author_addr_list:   # type: AuthorAddrInfo
    #         author_addr.addr_info = make_addr_by_country(author_addr.country, author_addr.addr)
    #         pass

    def output_item_au_addr(self, ut_char):
        with open(FilePathDef.ITEM_AU_ADDR_FILE_PATH, 'a') as fs:
            for addr_inst in self.author_addr_list:
                addr_inst.output_au_addr(fs, ut_char)
            pass
        pass

    def get_country_num(self):
        country_set = set()
        for addr_inst in self.author_addr_list:         # type: AuthorAddrInfo
            if addr_inst.country not in country_set:
                country_set.add(addr_inst.country)
        return len(country_set)

    def get_aff_num(self):
        aff_set = set()
        for addr_inst in self.author_addr_list:         # type: AuthorAddrInfo
            if addr_inst.au_grp_seq not in aff_set:
                aff_set.add(addr_inst.au_grp_seq)
        return len(aff_set)

    def get_first_addr(self):
        return self.author_addr_list[0]
