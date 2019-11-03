import os
import multiprocessing
import datetime
import shutil

from utils.Config.Config import Config
from utils.GetFunctions.GetFunctions import get_range

'''
This tool runs AFL with multiprocessing on given program
This tool uses config options:
  afl output path
  afl program path
  afl target relative path
  afl target option
'''

def run_afl(indexlist, cores, timeout, afl_output_path, program_path, target_relative_path, afl_target_option):
    pool= multiprocessing.Pool(cores)
    pool.map(run_afl_subprocess, (indexlist,timeout, afl_output_path, program_path, target_relative_path, afl_target_option))
    pool.close()
    pool.join()
    return

def run_afl_subprocess(index,timeout, afl_output_path, program_path, target_relative_path, afl_target_option):
    arg = "AFL_USE_ASAN=1 timeout %s afl-fuzz -m none -i %s -o %s %s/%s %s" % (timeout, "%s/afl_outcomes/afl_in" % afl_output_path, "%s/afl_outcomes/afl_out_%d" % (afl_output_path ,index), program_path, target_relative_path, afl_target_option)
    print(arg)
    with open("%s/afl_outcomes/start_time_%d" % (afl_output_path, index), "w+") as st:
        st.write(str(datetime.datetime.now()))
        
    afl_pipe = os.popen(arg)
    afl_pipe.read()
    afl_pipe.close()
    print("AFL run #%d has ended" % index)

if __name__ == '__main__':
    lower, upper = get_range()
    
    config = Config()

    global timeout 
    timeout = config.get_config("timeout")

    global afl_output_path
    afl_output_path = config.get_afl_output_path()
    
    global program_path
    program_path = config.get_config("afl program path")

    global target_relative_path
    target_relative_path = config.get_config("target relative path")

    global afl_target_option
    afl_target_option = config.get_afl_target_option()
    
    indexlist = list(range(lower, upper+1))
    run_afl(indexlist, upper-lower+1, timeout, afl_output_path, program_path, target_relative_path, afl_target_option)
