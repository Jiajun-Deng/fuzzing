class TimedInput:

    def __init__(self, afl_id, iid, timedelta, commit):
        self.afl_id = afl_id
        self.iid = iid
        self.time_delta = timedelta
        self.commit = commit

    def get_time_delta(self):
        return self.time_delta

    def get_commit(self):
        return self.commit

    def get_afl_id(self):
        return self.afl_id

    def get_iid(self):
        return self.iid

    def __cmp__(self, other):
        return self.time_delta - other.time_delta

    def __le__(self, other):
        return self.time_delta <= other.time_delta

    def __lt__(self, other):
        return self.time_delta < other.time_delta
