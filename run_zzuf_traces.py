import os, signal
import sys
import multiprocessing
import subprocess
import random

import utils.Operations.Operations as op
    
def init_process(core_index, test_path):
    outcomes_path = "%s/outcomes-%d" % (test_path, core_index)
    dir_existed = op.mkdir(outcomes_path)
    
    if dir_existed:
        op.mkdir("%s/out" % outcomes_path)
        op.mkdir("%s/err" % outcomes_path)
        
    else:
        print("%s already exists" % outcomes_path)
    
def fuzzing_process(core_index, seed_index, test_path,program_path, seed_path):

    outcomes_path = "%s/outcomes-%d" % (test_path,core_index)

    fuzzing_arg = "zzuf -r 0.01:0.9 -s %s <%s > %s/out/output" % (seed_index, seed_path, outcomes_path)

    fuzzing_return = subprocess.Popen(fuzzing_arg, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
    test_arg = "%s < %s/out/output" % (program_path, outcomes_path)
    test_return = subprocess.Popen(test_arg, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out,err=test_return.communicate()
    
    if err:
        print("ERROR #%d" % seed_index)
        print(err)
        test_input_path = "%s/out/output" % outcomes_path
        err_destination = "%s/err/id_%d;timestamp_%s" % (outcomes_path,seed_index, op.get_now_timestamp())
        op.copyfile(test_input_path, err_destination)
    else:
        print("seed_index: %d" % seed_index)


def run_zzuf_subprocess(core_index,test_path,program_path, seed_path):
    
    init_process(core_index, test_path)
    
    while True:
        seed_index = random.randint(0,sys.maxsize)
        fuzzing_process(core_index, seed_index, test_path, program_path, seed_path)

def run_fuzzer_with_alarm(core_index, test_path, program_path,seed_path, timeout):
    try:
        signal.signal(signal.SIGALRM,handler)
        signal.alarm(timeout)
        run_zzuf_subprocess(core_index, test_path, program_path, seed_path)
    except Exception as e:
        print(e)
    finally: 
        signal.alarm(0)
    print("Alarm wrapper for run_fuzzer_subprocess # %d ends" % core_index)  #alarm ends
     
'''
Use an alarm to control when to kill a process.
Work inside a process.
'''
def handler(signum, frame):
    raise Exception("timeout...") #when the alarm ends, call handler.

'''
Use multiprocessing.Pool to run several processes at the same time.
@param:
indexlist: a list of core index
cores: how many cores are used.
'''
def parallel_run_zzuf_with_timeout (indexlist, cores, test_path, program_path, seed_path, timeout):
    pool= multiprocessing.Pool(cores)
    try:
        for i in indexlist:
            pool.apply_async(func = run_fuzzer_with_alarm, args = (i,test_path, program_path, seed_path, timeout,))
    except Exception as e:
        print(e)
    pool.close()
    pool.join()
        