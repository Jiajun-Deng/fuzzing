import os
import sys
import datetime
import shutil
import subprocess


def get_now_timestamp():
    time_now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(time_now)
    return str(timestamp)
 
'''
Make a dir, if its parent dir doesn't exist, create it.
If the dir already exists, ERROR
path: the dir to make
'''
def mkdir(path):
    path = path.strip() #remove the begining spaces
    path = path.rstrip("\\") #remove spaces in the end
    isExist = os.path.exists(path) #Determine whether a path exists or not.
    if not isExist:
        print (path + " was successfully created.")
        os.makedirs(path)
        return True
    else:
        return False
    
def rmdir(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("ERROR: %s - %s." % (e.filename, e.strerror))
    
def copyfile(source, dest):
    if os.path.isfile(source):
        shutil.copyfile(source, dest)
        print("copy %s" % (source))
    else:
        print("ERROR: %s is not an valid file." % source)

def run_cmd(cmd):
    
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return p
