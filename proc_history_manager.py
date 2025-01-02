import os
from common_def import FilePathDef


class ProcHistoryMgr:
    def __init__(self):
        self.proc_history_uts = set()

    def load_history_uts(self):
        if not os.path.exists(FilePathDef.PROC_HISTORY_UTS_FILE_PATH):
            return
        with open(FilePathDef.PROC_HISTORY_UTS_FILE_PATH, 'r') as fs:
            for line_str in fs:
                split_lines = line_str.split('|')
                ut = split_lines[0].strip()
                if ut not in self.proc_history_uts:
                    self.proc_history_uts.add(ut)

    def is_ut_in_proc_history(self, ut: str):
        return ut in self.proc_history_uts

    def remove_ut(self, ut: str):
        self.proc_history_uts.remove(ut)


proc_history_mgr = ProcHistoryMgr()


def load_history_uts():
    proc_history_mgr.load_history_uts()


def is_ut_in_proc_history(ut: str):
    return proc_history_mgr.is_ut_in_proc_history(ut)


def remove_ut_history(ut: str):
    proc_history_mgr.remove_ut(ut)
