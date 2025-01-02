from paper_parser import PaperInfo
from paper_parser import get_ut_by_dict_data
from proc_history_manager import is_ut_in_proc_history
import os

RESULT_TITLE = "PT,AU,BA,BE,GP,AF,BF,CA,TI,SO,SE,BS,LA,DT,CT,CY,CL,SP,HO,DE,ID,AB,C1,RP,EM,RI,OI,FU,FX,CR,NR,TC,Z9," \
               "U1,U2,PU,PI,PA,SN,EI,BN,J9,JI,PD,PY,VL,IS,PN,SU,SI,MA,BP,EP,AR,DI,D2,EA,PG,WC,SC,GA,UT,PM,OA,HC,HP,DA"
KEYS_LIST_TEMPLATE = RESULT_TITLE.split(',')
RESULT_TITLE_START_PATTERN = "PT"
PAPER_INPUT_UNIQ_DIR = "paper_input_uniq"
PAPER_INPUT_SRC_DIR = "paper_input_src"
PAPER_OUTPUT_DIR = "paper_output"
PAPER_INFO_DICT = list()


def paper_info_output_tmp_data(dict_data: dict, data_idx: int, line_str: str, use_template_keys_list: bool,
                               title_list: list):
    output_file_path_tmp = os.path.join(os.getcwd(), PAPER_OUTPUT_DIR, "data_split_tmp.txt")
    open_flag = 'w'
    if data_idx > 1:
        open_flag = 'a'
    output_file_fs = open(output_file_path_tmp, open_flag)
    output_file_fs.write("data_idx: " + str(data_idx) + "\n")
    for key, value in dict_data.items():
        output_file_fs.write(key + ": " + value + "\n")
        output_file_fs.write("\n")
    output_file_fs.close()


def paper_info_proc(dict_data: dict, data_idx: int, line_str: str, use_template_keys_list: bool, title_list: list):
    ut_char = get_ut_by_dict_data(dict_data)
    if is_ut_in_proc_history(ut_char):
        print("ut {} is proced".format(ut_char))
        return
    paper_info = PaperInfo()
    paper_info.load_by_data(dict_data)
    paper_info.output_data()


def load_paper_info_file(file_path: str, load_proc):
    keys_list = None
    data_idx = 1
    use_template_keys_list = False
    with open(file_path) as fs:
        print("file path %s format" % file_path)
        for lines in fs:
            dict_data = None
            line_str = lines.strip()
            split_data = line_str.split('\t')
            if keys_list is None:
                # 第一列为PT的话，那么就判定为title
                split_data[0] = split_data[0].strip()
                # 清理掉脏符号
                if split_data[0].startswith("\ufeff"):
                    split_data[0] = split_data[0].replace("\ufeff", "")
                print("title {} vs {}".format(split_data[0], RESULT_TITLE_START_PATTERN))
                if split_data[0] == RESULT_TITLE_START_PATTERN:
                    # 如果第一行是title的话，那么直接把分割好的数据给keys_list
                    keys_list = split_data
                else:
                    # 不然的话把预设的title赋给keys_list
                    keys_list = KEYS_LIST_TEMPLATE
                    use_template_keys_list = True
                    # 如果是数据的话，要把第一行数据补上
                    dict_data = dict(zip(keys_list, split_data))
                print("file {}, title is {}, use_template_keys_list {}".format(file_path, keys_list,
                                                                               use_template_keys_list))
            else:
                dict_data = dict(zip(keys_list, split_data))
            if dict_data:
                try:
                    load_proc(dict_data, data_idx, line_str, use_template_keys_list, keys_list)
                except Exception as e:
                    print("Err: {}".format(e))
                    print("Exception line: {}".format(line_str))
                    raise e
                    # 直接输出，不需要存储
                # PAPER_INFO_DICT.append(paper_info)
                # paper_info_output_tmp_data(data_idx, dict_data)
                # data_idx += 1
                # for key, value in dict_data.items():
                #     pass
                pass
            pass
    pass


def load_paper_input_dir(dir_path: str, load_proc):
    for dir_v in os.listdir(dir_path):
        dir_tmp = os.path.join(dir_path, dir_v)
        if os.path.isdir(dir_tmp):
            # 说明还是目录，那么继续遍历目录
            load_paper_input_dir(dir_tmp, load_proc)
        else:
            if dir_v.startswith(".DS_Store"):
                continue
            # elif dir_v.startswith("result_"):
            # 说明是要找的文件，那么进行解析
            load_paper_info_file(dir_tmp, load_proc)
    pass


def load_paper_input(load_proc, paper_input_dir):
    # 先遍历目录，找到所有的文件名
    paper_input_path = os.path.join(os.getcwd(), paper_input_dir)
    load_paper_input_dir(paper_input_path, load_proc)
    pass
