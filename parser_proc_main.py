from paper_info_load_api import load_paper_input
from paper_info_load_api import paper_info_proc
from paper_info_load_api import PAPER_INPUT_UNIQ_DIR
from proc_history_manager import load_history_uts
from state_code_analysis import load_state_code

if __name__ == '__main__':
    load_state_code()
    load_history_uts()
    load_paper_input(paper_info_proc, PAPER_INPUT_UNIQ_DIR)
    # paper_info = PaperInfo()
    pass
