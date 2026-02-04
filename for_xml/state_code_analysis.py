
state_code_set = set()


def load_state_code():
    state_code_file_path = "postcode_usa.csv"
    with open(state_code_file_path, 'r') as fs:
        for line_str in fs:
            line_split = line_str.strip().split(',')
            state_code_set.add(line_split[1])


def is_state_code(test_str):
    return test_str in state_code_set
