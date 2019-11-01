import os


class Commit:

    def __init__(self, index, hash, path=""):
        self.index = index
        self.id = hash
        self.path = path
        self.name = "%d_%s" % (self.index, self.id)
        self.compiled = True

    def get_name(self):
        return self.name

    def get_status(self):
        return self.compiled

    def get_index(self):
        return self.index

    def get_id(self):
        return self.id

    def get_hash(self):
        return self.get_id(self)

    def get_path(self):
        return self.path

    def set_status(self, success):
        self.compiled = success


def read_commits(commit_path):
    print("read commit numbers -------- start")

    if not os.path.exists(commit_path):
        print("read commit numbers -------- cannot find file")
        exit(1)
    with open(commit_path) as file:
        # each line stores a commit id
        lines = file.readlines()

    if len(lines) == 0:
        print("read commit numbers -------- file is empty")
    # remove ending '\n'
    for i in range(0, len(lines)):
        lines[i] = lines[i][:-1]
    print("read commit numbers -------- finish")
    commits = []
    i = 1
    for id in lines:
        commits.append(Commit(i, id))
        i += 1
    return commits
