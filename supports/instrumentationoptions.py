from supports.config import Config
from supports.read_buglist import read_buglist


class InstrumentationOption:

    def __init__(self, folder_name, option_list):
        self.folder_name = folder_name
        self.option_list = option_list

    def get_name(self):
        return self.folder_name

    def get_options(self):
        return self.option_list


def build_ins_options():
    config = Config()
    buglist = read_buglist(config.get_config("buglist path"))

    bug_options = []
    for i in range(len(buglist)):
        l = {}
        for b in buglist:
            l[b] = 0;
        l[buglist[i]] = 1;
        bug_options.append(InstrumentationOption(buglist[i], l))
    return bug_options
