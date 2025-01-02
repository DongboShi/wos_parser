import os
from paper_info_load_api import load_paper_input
from paper_info_load_api import PAPER_INPUT_SRC_DIR
from paper_info_load_api import paper_info_output_tmp_data
from paper_info_load_api import KEYS_LIST_TEMPLATE


PAPER_OUTPUT_DIR = "paper_input_uniq"
RESULT_FILE_NAME = "result_paper_info_uniq.txt"
RESULT_FILE_NAME_NO_UT = "paper_info_no_ut.txt"
RESULT_FILE_NAME_NO_TITLE = "result_paper_info_uniq_no_title.txt"
PAPER_UT = set()


def paper_info_proc(dict_data: dict, data_idx: int, line_str: str, use_template_keys_list: bool, title_list: list):
    if "UT" not in dict_data:
        # print("UT not found in line:\n%s\n" % line_str)
        uniq_output_path = os.path.join(os.getcwd(), PAPER_OUTPUT_DIR, RESULT_FILE_NAME_NO_UT)
        with open(uniq_output_path, 'a') as fs:
            fs.write("%s\n" % line_str)
        return
    split_str_arr = dict_data["UT"].split(":")
    if len(split_str_arr) < 2:
        print("UT not found in:{}\nUT:{}\n".format(dict_data, dict_data["UT"]))
        paper_info_output_tmp_data(dict_data, 1, "", False, title_list)
        uniq_output_path = os.path.join(os.getcwd(), PAPER_OUTPUT_DIR, RESULT_FILE_NAME_NO_UT)
        with open(uniq_output_path, 'a') as fs:
            fs.write("%s\n" % line_str)
        return
    ut_char = split_str_arr[1]
    if ut_char in PAPER_UT:
        return
    PAPER_UT.add(ut_char)
    result_file_name_str = ""
    if use_template_keys_list:
        result_file_name_str = RESULT_FILE_NAME_NO_TITLE
    else:
        result_file_name_str = RESULT_FILE_NAME
    # 把列的数量作为文件的前缀
    result_file_name_str = "{}_{}".format(len(title_list), result_file_name_str)
    uniq_output_path = os.path.join(os.getcwd(), PAPER_OUTPUT_DIR, result_file_name_str)
    if not os.path.isfile(uniq_output_path):
        # 文件不存在，那么先把头写进去
        with open(uniq_output_path, 'a') as fs:
            is_first_title = True
            for title_str in title_list:
                if is_first_title:
                    is_first_title = False
                else:
                    fs.write("\t")
                fs.write(title_str)
            fs.write('\n')
    # 写具体数据
    with open(uniq_output_path, 'a') as fs:
        fs.write("%s\n" % line_str)


if __name__ == '__main__':
    load_paper_input(paper_info_proc, PAPER_INPUT_SRC_DIR)
    # paper_info = PaperInfo()
    pass
