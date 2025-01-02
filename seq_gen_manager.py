
ITEM_AU_ADDR_KEY = "item_au_addr"


class SeqGenManager:
    def __init__(self):
        self.seq_dict = dict()

    def seq_gen(self, seq_key: str):
        if seq_key not in self.seq_dict:
            self.seq_dict[seq_key] = 0
        self.seq_dict[seq_key] += 1
        return self.seq_dict[seq_key]
