from paper_info_load_api import load_paper_input
from paper_info_load_api import paper_info_proc
from paper_info_load_api import PAPER_INPUT_UNIQ_DIR
from proc_history_manager import load_history_uts
from state_code_analysis import load_state_code
from parallel_processor import process_with_concurrency
import argparse


def run_parser():
    """Entry point with sequential or concurrent execution modes"""
    arg_parser = argparse.ArgumentParser(description='WOS Parser - Process Web of Science data')
    arg_parser.add_argument('--parallel', action='store_true', 
                           help='Enable concurrent processing')
    arg_parser.add_argument('--workers', type=int, default=None,
                           help='Worker count for parallel mode (default: auto-detect)')
    
    options = arg_parser.parse_args()
    
    load_state_code()
    load_history_uts()
    
    if options.parallel:
        print("==> Concurrent processing mode active")
        process_with_concurrency(paper_info_proc, PAPER_INPUT_UNIQ_DIR, workers=options.workers)
    else:
        print("==> Sequential processing mode active")
        load_paper_input(paper_info_proc, PAPER_INPUT_UNIQ_DIR)


if __name__ == '__main__':
    run_parser()
