from common_def import FilePathDef
from common_def import OUTPUT_FILE_SEPARATOR

class FUInfo:
    def __init__(self, grant, grant_code):
        self.grant = grant
        self.grant_code = grant_code

    def output_data(self, fs, ut_char):
        # ut_char, grant, grant_code
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}\n".format(OUTPUT_FILE_SEPARATOR, ut_char, self.grant, self.grant_code))


class FUManager:
    def __init__(self):
        self.fu_list = list()

    def load(self, fu, ut_char):
        if len(fu) > 0:
            fu_split_arr = fu.split(";")
            for fu_str in fu_split_arr:
                grant_str_arr = fu_str.split("[")
                grant = grant_str_arr[0].strip()
                g_code = ""
                if len(grant_str_arr) >= 2:
                    g_code = grant_str_arr[1].strip().replace("]", "")
                if g_code.find(","):
                    for code in g_code.split(","):
                        grant_code = code.strip()
                        self.fu_list.append(FUInfo(grant, grant_code))
                else:
                    grant_code = g_code.strip()
                    self.fu_list.append(FUInfo(grant, grant_code))
        else:
            print("The FU is null")
        pass

    def output_data(self, ut_char):
        with open(FilePathDef.ITEM_GRANT_FILE_PATH, 'a') as fs:
            for fu_inst in self.fu_list:                # type: FUInfo
                fu_inst.output_data(fs, ut_char)
        pass
