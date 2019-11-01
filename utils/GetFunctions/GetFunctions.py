import re

def get_core_number():
    n = 0
    while n <= 0:
        n = int(input("Enter number of cores to use:\n"))
    return n

def get_range():
    lower = 1
    upper = 0
    while lower > upper:
        lower = int(input("Enter the lower index:\n"))
        upper = int(input("Enter the upper index:\n"))
    return (lower, upper)


def read_buglist(buglist_path):
    buglist = []
    with open(buglist_path) as file:
        lines = file.readlines();
        for l in lines:
            if re.match("/\*.*?\*/", l[:-1]):
                continue
            buglist.append(l[:-1])
    return buglist
