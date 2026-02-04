import re
from state_code_analysis import is_state_code

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


class AddressInfo:
    def __init__(self):
        self.state = ""
        self.zip = ""
        self.city = ""

    def load_addr(self, addr):
        pass

    def update(self, city, zip_str, state):
        self.city = city
        self.zip = zip_str
        self.state = state


class ChinaAddressInfo(AddressInfo):
    STATE_SPECIAL = ["Beijing", "Tianjin", "Shanghai", "Chongqing", "Hong Kong", "Macao"]

    def __init__(self):
        super(ChinaAddressInfo, self).__init__()

    def get_city_or_province(self, loc):
        province_found = False
        global CHINESE_PROVINCE_LIST
        for p in CHINESE_PROVINCE_LIST:
            if p.lower() in re.sub(r'\s{2,}', ' ', loc.lower()):
                self.state = p
                province_found = True
                break
        if not province_found or self.state in self.STATE_SPECIAL:
            self.city = re.sub(r"'", "_", loc.strip())
            self.city = re.sub(r"\\", "", self.city)

    def get_zip_code_and_other(self, part):
        temp_list = part.split(" ")
        for i in temp_list:
            if re.findall(r'\d', i):
                self.zip = re.findall(r'\d+', i)[0]
                other = re.sub(r'\s{2,}', ' ', part.replace(i, "")).strip()
                break
        self.get_city_or_province(other)

    def load_addr(self, addr):
        parts = addr.split(", ")

        if re.findall(r'\d', parts[-2]):
            self.get_zip_code_and_other(parts[-2])
        else:
            self.get_city_or_province(parts[-2])
        if self.city or self.zip or self.state in self.STATE_SPECIAL:
            pass
        else:
            # print("addr: {}".format(addr))
            # print(parts)
            if re.findall(r'\d', parts[-3]):
                self.get_zip_code_and_other(parts[-3])
            elif len(re.findall(r'\s', parts[-3])) <= 1:
                self.get_city_or_province(parts[-3])
        pass


class USAAddressInfo(AddressInfo):
    def __init__(self):
        super(USAAddressInfo, self).__init__()
        self.country = ""

    def load_addr(self, addr):
        # 美国详细地址
        if not addr.endswith("USA"):
            return

        parts = addr.split(",")
        last_part = parts[-1].strip()
        parts_split_arr = last_part.split(" ")
        if re.findall(r"\d", last_part):
            self.city = parts[-2].strip()
            self.state = parts_split_arr[0].strip()
            self.country = parts_split_arr[-1].strip()
            if len(parts_split_arr) == 3:
                self.zip = parts_split_arr[1].strip()
            else:
                self.zip = parts_split_arr[1].strip() + parts_split_arr[2].strip()
        else:
            if last_part != "USA":
                print("addr {}, parts split {}".format(addr, parts_split_arr))
                self.state = parts_split_arr[0]
                self.country = parts_split_arr[-1]
                # self.state, self.country = tuple(parts_split_arr)
                self.city = parts[-2].strip()
            else:
                # print(addr)
                # print(parts)
                # print(parts[-2])
                if is_state_code(parts[-2]):
                    self.state = parts[-2]
                    self.country = "USA"
                else:
                    self.state, self.country = tuple(parts[-2].strip().split(" "))
                self.city = parts[-3].strip()


def make_addr_by_country(country: str, addr: str):
    addr_info = None
    if country == "USA":
        addr_info = USAAddressInfo()
    elif country == "Peoples R China":
        addr_info = ChinaAddressInfo()

    if addr_info:
        addr_info.load_addr(addr)

    return addr_info
    pass
