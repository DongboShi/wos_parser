
INPUT_FILE_PATH = "paper_input/test_input.txt"
MATCH_KEY = "C1"

if __name__ == '__main__':
    title_keys = None
    match_title_idx = 0
    with open(INPUT_FILE_PATH, 'r') as fs:
        for line_str in fs:
            if title_keys is None:
                title_keys = line_str.split('\t')
                idx_tmp = 0
                for title in title_keys:
                    print("{}\n".format(title))
                    if title == MATCH_KEY:
                        match_title_idx = idx_tmp
                        print("idx: {}\n".format(match_title_idx))
                        break
                    idx_tmp += 1
            else:
                data_arr = line_str.split('\t')
                print("{}: {}\n".format(MATCH_KEY, data_arr[match_title_idx]))
