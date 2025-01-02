from common_def import OUTPUT_FILE_SEPARATOR

class AuthorName:
    def __init__(self, name, au_seq):
        name_lists = name.split(",")
        self.name = name
        self.sur_name = name_lists[0].strip()
        self.given_name = name_lists[-1].strip()
        self.middle_name = ""
        self.au_seq = au_seq
        if len(name_lists) > 1:
            self.middle_name = name_lists[1].strip()

    def output_author(self, fs, ut):
        # auseq, ut_char, name, surname, middlename, givenname
        if fs is None:
            return
        # fs.write("%s|%s|%s|%s|%s|%s\n" % (self.au_seq, ut, self.name, self.sur_name, self.middle_name, self.given_name))
        fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}\n".format(OUTPUT_FILE_SEPARATOR, self.au_seq, ut, self.name, self.sur_name, self.given_name))
