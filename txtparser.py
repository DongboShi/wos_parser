#!/usr/bin/env python
# -*- coding: utf-8 -*-

# WC与SC对应了两个分类系统，现在做了SC的，还需要单独补充一个WC的分类
# OA 与 PM， HC 字段加一下，就是加表
# 拆分item_author出现神奇的情况，例如000238442600072，需要检查
# item_author有空缺，需要改改A1997WT21300049


# 此处说明
# 新添加函数getitemfield2


import numpy as np
import hashlib
import re
# 读入数据
def loadbib(file):
    woslist = list()
    with open(file,"r") as f:
        key = f.readlines()[0].replace("\n","").split("\t")
    with open(file,"r") as f:
        for line in f.readlines()[1:(len(f.readlines())-1)]:
            field = line.replace("\n","").split("\t")
            woslist.append(dict(zip(key,field)))
    return(woslist)

# 解析表格名字
def getauthor(UT, AF):
    UT = UT.split(":")[1]
    author = AF.split("; ")
    authorlist = list()
    ut_char = UT
    n = 1
    for name in author:
        auseq = n
        surname = name.split(",")[0].strip()
        if(name.count(",") == 1):
            givenname = name.split(",")[1].strip()
            middlename = None
        else:
            givenname = name.split(",")[-1].strip()
            middlename = name.split(",")[1].strip()
        namedict = {"auseq":auseq,"ut_char":ut_char,"name":name,
                    "surname":surname, "middlename":None, "givenname":givenname}
        authorlist.append(namedict)
        n += 1
    return(authorlist)

# 拆分地址字段
def split_c1(c1):
    if c1 != '':
        # 解决存在[wang,[liu]]这种格式数据的问题，删除中嵌套的[]
        if re.findall(r"\[[^(\[)]+?\[[^(\[)]+?\][^(\[)]*?\]",c1):
            iterc1 = re.finditer(r"\[[^(\[)]+?\[[^(\[)]+?\][^(\[)]*?\]", c1)
            for p in iterc1:
                old = p.group()
                pt = re.findall(r"\[[^(\[)]+?\]", old)[0]
                npt = re.sub('(\[)|(\])', '', pt)
                new = old.replace(pt, npt)
                c1 = c1.replace(old, new)
        if "[" in c1:
            au_addr_info = []
            complete_queue = re.split(r"\[", c1)
            complete_queue.pop(0)
            augrpseq = 1
            for i, p in enumerate(complete_queue, start=1):
                if "]" in p:
                    au = re.split(r"\]",p)[0]
                    authors = au.split(";")
                    address = re.split(r"\]",p)[1]
                    #addr = re.findall(r"\[([\s\S]+?)\]\s*([\s\S]+?)(?:;|$)", p)[0]
                    addrs = address.strip().split(";")
                    addrs = list(filter(None, addrs))
                    for addr in addrs:
                        for author in authors:
                            addr = re.sub(';','',addr).strip()
                            addr = re.sub('|','',addr)
                            author = author.strip()
                            country = addr.split(",")[-1]
                            addr_md5 = hashlib.md5()
                            addr_md5.update(addr.encode(encoding="utf-8"))
                            addrs_md5 = addr_md5.hexdigest()
                            if country.endswith("USA"):
                                country = "USA"
                            au_addr_info.append({
                                "au": author,
                                "addr": addr,
                                "country": country,
                                "augrpseq": augrpseq,
                                "addr_md5":addrs_md5
                            })
                        augrpseq = augrpseq + 1
                else:
                    au_addr_info.append({
                        "au": p,
                        "addr": None,
                        "country": None,
                        "augrpseq": augrpseq,
                        "addr_md5": None
                    })
            return au_addr_info
        else:
            au_addr_info = []
            addrs = c1.split("; ")
            for i, addr in enumerate(addrs, start=1):
                addr = re.sub(';','',addr).strip()
                addr = re.sub('|','',addr)
                addr_md5 = hashlib.md5()
                addr_md5.update(addr.encode(encoding="utf-8"))
                addrs_md5 = addr_md5.hexdigest()
                country = addr.split(",")[-1].strip()
                if country.endswith("USA"):
                    country = "USA"
                au_addr_info.append({"au": None, "addr": addr, "country": country, "augrpseq": i,"addr_md5":addrs_md5})
            return au_addr_info

# 解析地址表格
def make_item_au_addr(UT, C1):
    UT = UT.split(":")[1]
    addr = split_c1(C1)
    addlist = list()
    if addr:
        for add in addr:
            add["ut_char"] = UT
            addlist.append(add)
    return (addlist)
# 美国详细地址
def getUSADetail(address):
    result = dict()
    if address.endswith("USA"):
        parts = address.split(",").strip()
        if re.findall(r"\d", parts[-1]):
            city = parts[-2]
            if(len(parts[-1].split(" "))==3):
                state_code, zip_code, country = list(parts[-1].split(" "))
            else:
                parts_tmp = parts[-1].split(" ")
                state_code = parts_tmp[0]
                country = parts_tmp[-1]
                zip_code = parts_tmp[1]+parts_tmp[2]
            result.update({"state":state_code, "zip":zip_code, "country":country})
        else:
            if parts[-1] != "USA":
                state_code, country = tuple(parts[-1].split(" "))
                city = parts[-2]
            else:
                state_code, country = tuple(parts[-2].split(" "))
                city = parts[-3]
            result.update({"state":state_code, "country":country})
        result.update({"city":city})
        return result
# 中国详细地址
CHINESE_PROVINCE_LIST = [
    "Beijing","Tianjin","Shanghai","Chongqing",
    "Hebei","Henan","Yunnan","Liaoning","Heilongjiang",
    "Hunan","Anhui","Shandong","Xinjiang","Jiangsu",
    "Zhejiang","Jiangxi","Hubei","Guangxi","Gansu",
    "Shanxi","Inner Mongolia","Shaanxi","Jilin","Fujian",
    "Guizhou","Guangdong","Qinghai","Tibet","Sichuan",
    "Ningxia","Hainan","Hong Kong","Macao"
]

def getChinaDetail(address):
    def getCityOrProvince(loc):
        result = dict()
        province_found = False
        global CHINESE_PROVINCE_LIST
        for p in CHINESE_PROVINCE_LIST:
            if p.lower() in re.sub(r'\s{2,}',' ',loc.lower()):
                result["state"] = p
                province_found = True
                break
        if not province_found or result["state"] in ["Beijing","Tianjin","Shanghai","Chongqing","Hong Kong","Macao"]:
            result["city"] = re.sub(r"'","_",loc.strip())
            result["city"] = re.sub(r"\\","",result["city"])
        return result

    def getZipCodeAndOther(part):
        result = {}
        temp_list = part.split(" ")
        for i in temp_list:
            if re.findall(r'\d', i):
                result["zip"] = re.findall(r'\d+', i)[0]
                other = re.sub(r'\s{2,}', ' ', part.replace(i,"")).strip()
                break
        result.update(getCityOrProvince(other))
        return result

    result = dict()
    parts = address.split(", ")

    if re.findall(r'\d', parts[-2]):
        result.update(getZipCodeAndOther(parts[-2]))
    else:
        result.update(getCityOrProvince(parts[-2]))
    if "city" in result or "zip" in result or result["state"] in ["Beijing","Tianjin","Shanghai","Chongqing","Hong Kong","Macao"]:
        return result
    else:
        if re.findall(r'\d', parts[-3]):
            result.update(getZipCodeAndOther(parts[-3]))
        else:
            if len(re.findall(r'\s', parts[-3])) <= 1:
                result.update(getCityOrProvince(parts[-3]))
            else:
                pass
    return result
# 解析参考文献
def getref(UT, CR):
    UT = UT.split(":")[1]
    ut_char = UT
    refs = CR.split(";").strip()
    reflist = list()
    for ref in refs:
        authors = ref.split(",")[0].strip()
        year = ref.split(",")[1].strip()
        #venue = ref.split(", ")[2]
        if(ref.count("DOI ")):
            DOI = ref.split(",")[-1].strip()
        else:
            DOI = None
        if(ref.count(",") >= 2):
            venue = ref.split(",")[2].strip()
        else:
            venue = None
        if(ref.count(",") >= 3):
            volume = re.findall(r'\d+',ref.split(",")[3])[0].strip()
        else:
            volume = None
        if(ref.count(",") >= 4):
            page = re.findall(r'\d+',ref.split(",")[4])[0].strip()
        else:
            page = None
        refdict = {"ut_char":ut_char,"ref":ref, "authors":authors,
                   "year":year, "venue":venue, "DOI":DOI, "volume":volume, "page":page}
        reflist.append(refdict)
    return(reflist)
# 论文标题
def getitemtitle(UT,TI):
    UT = UT.split(":")[1]
    result = list()
    ti_dict = {"ut_char":UT,"ti":TI}
    result.append(ti_dict)
    return(result)
# 论文摘要
def getitemabs(UT,AB):
    UT = UT.split(":")[1]
    result = list()
    ab_dict = {"ut_char":UT,"abstract":AB}
    result.append(ab_dict)
    return(result)
# 论文杂志
def getitemjournal(UT,SO,J9,JI,SN,PY):
    UT = UT.split(":")[1]
    result = list()
    j_dict = {"ut_char":UT,"SO":SO,"J9":J9,"JI":JI,"SN":SN,"pub_year":PY}
    result.append(j_dict)
    return(result)
# 论文资助
def getitemgrant(UT,FU):
    UT = UT.split(":")[1]
    result = list()
    if len(FU) > 0:
        fulist = FU.split(";")
        for fu in fulist:
            grant = fu.split("[")[0].strip()
            g_code = fu.split("[")[1].strip().replace("]","")
            if(g_code.find(",")):
                for code in g_code.split(","):
                    grant_code = code.strip()
                    gr_dict = {"ut_char":UT,"grant":grant,"grant_code":grant_code}
                    result.append(gr_dict)
            else:
                grant_code = code.strip()
                gr_dict = {"ut_char":UT,"grant":grant,"grant_code":grant_code}
                result.append(gr_dict)
    else:
        print("The FU is null")
    return(result)
# 关键词
def getitemkw(UT,DE):
    UT = UT.split(":")[1]
    result = list()
    delist = DE.split(";")
    for de in delist:
        kw = de.strip()
        de_dict = {"ut_char":UT,"keyword":kw}
        result.append(de_dict)
    return(result)
# 扩展关键词
def getitemkwwd(UT,ID):
    UT = UT.split(":")[1]
    result = list()
    delist = ID.split(";")
    for de in delist:
        kw = de.strip()
        de_dict = {"ut_char":UT,"keyword":kw}
        result.append(de_dict)
    return(result)
# 研究领域
def getitemfield(UT,SC):
    UT = UT.split(":")[1]
    result = list()
    sclist = SC.split(";")
    for sc in sclist:
        fd = sc.strip()
        fd_dict = {"ut_char":UT,"field":fd}
        result.append(fd_dict)
    return(result)

# 领域切分的新函数
def getitemfield2(UT,WC):
    UT = UT.split(":")[1]
    result = list()
    wclist = WC.split(";")
    for wc in wclist:
        fd = wc.strip()
        fd_dict = {"ut_char":UT,"field":fd}
        result.append(fd_dict)
    return(result)

# 邮件地址
def getitemem(UT,EM):
    UT = UT.split(":")[1]
    result = list()
    emlist = EM.split(";")
    for em in emlist:
        email = em.strip()
        em_dict = {"ut_char":UT,"email":email}
        result.append(em_dict)
    return(result)

file = "/Users/birdstone/paper_crawler/output/2001_2007/JOURNAL OF MANAGEMENT INFORMATION SYSTEMS/result_1_305.txt"
result = loadbib(file)
# 新加入getitem函数

def getitem(UT,DT,PY,VL,IS,BP,EP,PG,TC,Z9,LA,DI,SN,AF,C1,NR):
    UT = UT.split(":")[1]
    numau = AF.count("; ")+1
    numaff = C1.count("; ")+1
    addr = split_c1(C1) # split_c1是在getitem_au_addr定义的函数 'country': 'SINGAPORE', 'augrpseq'
    if addr:
        country_list = list()
        augrp_list = list()
        for add in addr:
            if not add["country"] in country_list:
                   country_list.append(add["country"])
            augrp_list.append(add["augrpseq"])
        numctry = len(country_list)
        numaff = max(augrp_list)
    else:
        numaff = 0
        numctry = 0
    result = list()
    result_dict = {"ut_char": UT,
    "item_type":DT,
    "pub_year":PY,
    "volume":VL,
    "issue":IS,
    "first_pg":BP,
    "last_pg":EP,
    "pages":PG,
    "num_country":numctry,
    "cite_count":TC,
    "cite_count_wide":Z9,
    #"impactart":None,
    "lang":LA,
    "doi":DI,
    #"field":None,
    "num_au":numau,
    "num_afid":numaff,
    #"codencode":None,
    "ref_count":NR,
    #"source_id":None,
    "issn":SN}
    result.append(result_dict)
    return(result)

# 新加入的ref拆分与局
def getref(UT, CR):
    UT = UT.split(":")[1]
    ut_char = UT
    refs = CR.split("; ")
    journal_ref_list = list()
    patent_ref_list = list()
    book_ref_list = list()
    reflist = list()
    for ref in refs:
        if(re.match(r'.*,.\d{4},.*,.V\d+,.P\d+.*',ref)):
            authors = ref.split(",")[0].strip()
            year = ref.split(",")[1].strip()
            venue = ref.split(",")[2].strip()
            volume = re.findall(r'\d+',ref.split(",")[3])[0].strip()
            page = re.findall(r'\d+',ref.split(",")[4])[0].strip()
            if(ref.count("DOI ")):
                DOI = re.sub(r'^DOI','',ref.split(",")[-1]).strip()
            else:
                DOI = None
            refdict = {"ut_char":ut_char,"ref":ref, "authors":authors, 
                   "year":year, "venue":venue, "DOI":DOI, "volume":volume, "page":page}
            journal_ref_list.append(refdict)
        elif(re.match(r'.*,.\d{4},.*Patent",ref',ref)):
            refdict = {"ut_char":ut_char,"ref":ref}
            patent_ref_list.append(refdict)
        elif(re.match(r'.*,.\d{4},.*',ref)):
            refdict = {"ut_char":ut_char,"ref":ref}
            book_ref_list.append(refdict)
    reflist = [journal_ref_list,patent_ref_list,book_ref_list]
    return(reflist)


# 此函数依赖于split_c1函数
# 目的是生成一个新的表，item_reprint
# 表的结构为（rpseq(通讯作者顺序), ut_char,name(通讯作者全名),surname, middlename,givenname，
# addr（通讯作者地址）,country(通讯地址国家), addr_md5）
# 表格repseq和ut_char构成联合主键

def getrpauthor(UT, RP):
    ut_char = UT.split(":")[1]
    rplist = list()
    if RP != "":
        n = 1
        if RP.count("(reprint author)") == 1 :
            name = RP.split("(reprint author),")[0].strip()
            surname = name.split(",")[0].strip()
            if(name.count(", ") == 1):
                givenname = name.split(",")[1].strip()
                middlename = None
            else:
                givenname = name.split(",")[-1].strip()
                middlename = name.split(",")[1].strip()
            addr = RP.split("(reprint author)")[1]
            country = split_c1(addr)[0]["country"].replace('.',"")
            if country.endswith("USA"):
                country = "USA"
            addr_md5 = split_c1(addr)[0]["addr_md5"]
            rpseq = n
            rpdict = {"rpseq":rpseq, "ut_char":ut_char,"name":name, 
                    "surname":surname, "middlename":middlename, "givenname":givenname,
                     "addr":addr, "country" : country, "addr_md5" : addr_md5}
            rplist.append(rpdict)
        if RP.count("(reprint author)") > 1 :
            RP = RP + ";"# 结尾增加一个；便于统一拆分
            pattern = re.compile(r'(.*?\(reprint author\).*?);') # 重新修改正则表达式的逻辑，使用非贪婪的匹配方法
            complete_queue = pattern.findall(RP)
            for rp in complete_queue :
                name = rp.split("(reprint author),")[0].strip()
                addr = rp.split("(reprint author)")[1]
                country = split_c1(addr)[0]["country"].replace('.',"")
                if country.endswith("USA"):
                    country = "USA"
                addr_md5 = split_c1(addr)[0]["addr_md5"]
                name_spl = name.split(";")# 当作者有两个名字时候，先行使用；拆分
                for name_sub in name_spl:
                    surname = name_sub.split(",")[0].strip()
                    if(name_sub.count(", ") == 1):
                        givenname = name_sub.split(",")[1].strip()
                        middlename = None
                    else:
                        givenname = name_sub.split(",")[-1].strip()
                        middlename = name_sub.split(",")[1].strip()
                    rpseq = n
                    rpdict = {"rpseq":rpseq, "ut_char":ut_char,"name":name_sub, 
                              "surname":surname, "middlename":middlename, "givenname":givenname,
                              "addr":addr, "country" : country, "addr_md5" : addr_md5}
                    rplist.append(rpdict)
                    n += 1
    return(rplist)




