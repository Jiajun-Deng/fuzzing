import datetime
import os
import pickle


class ErrorInput:

    def __init__(self, name, path):

        # name of the file contains some attribute information
        self.name = name
        # split file name to retrieve the information
        attributes = name.split(',')
        self.info = {}
        for str in attributes:
            attr = str.split(':')
            self.info[attr[0]] = attr[1]

        # stores path of the file
        self.path = path

        self.mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        self.mapping = []
        self.detection = []

    def __cmp__(self, other):
        return int(self.info['id']) - int(other.info['id'])

    def __le__(self, other):
        return int(self.info['id']) <= int(other.info['id'])

    def __lt__(self, other):
        return int(self.info['id']) < int(other.info['id'])

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def get_attr(self, attr):
        if attr in self.info:
            return self.info[attr]
        return None

    def get_id(self):
        return int(self.get_attr("id"))

    def get_mtime(self):
        return self.mtime

    def get_mapping(self):
        return self.mapping

    def add_mapping(self, cid):
        self.mapping.append(cid)

    def get_detection(self):
        return self.detection

    def add_detection(self, bid):
        self.detection.append(bid)


def read_inputs_from_file(input_path):
    inputs = []
    fileList = os.listdir(input_path)

    for file_name in fileList:
        if file_name != 'README.txt':
            inputs.append(ErrorInput(file_name, '%s/%s' % (input_path, file_name)))
    inputs.sort()
    return inputs


def read_inputs_from_pickle(pickle_path):
    with open(pickle_path, "rb+") as file:
        inputs = pickle.load(file)
    return inputs


def dump_inputs_into_pickle(inputs, pickle_path):
    with open(pickle_path, "wb+") as file:
        pickle.dump(inputs, file)
