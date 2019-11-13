import os, signal
import sys
import multiprocessing
import subprocess
import random

import utils.Operations.Operations as op
    
def init_process(core_index, work_path):
    dir_existed = op.mkdir(work_path)
    
    if dir_existed:
        op.mkdir("%s/output" % work_path)#mutations_path
        #op.mkdir("%s/input" % work_path)#dedup_path
        op.mkdir("%s/err" % work_path)#err_path

def fuzzing_process(core_index, seed_index, test_path,program_path, seed_path, i):

    fuzzing_arg = "zzuf -r 0.01:0.9 -s %s <%s > %s/outcomes-%d/output/output-%d" % (seed_index, seed_path, test_path, core_index, i)

    fuzzing_return = subprocess.Popen(fuzzing_arg, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
def testing_process(core_index, input_path, err_path, program_path):
    input_files = os.listdir("%s/" % input_path)
    
    for onefile in input_files:
        test_input = "%s/%s" % (input_path, onefile)
        test_cmd = "%s < %s" % (program_path, test_input)
        test_return = op.run_cmd(test_cmd)
        test_out, test_err = test_return.communicate()
    
        #If the input crashes the program, copy it to err/ dir.
        if test_err:
              print("ERROR input file: %s" % onefile)
              print(test_err)
              err_destination = "%s/%s;timestamp_%s" % (err_path, onefile, op.get_now_timestamp())
              op.copyfile(test_input, err_destination)

'''
Remove duplicates using afl-cmin.
'''
def de_dup_process(core_index, program_path, input_path, output_path):
    #remove duplicates using afl-cmin "afl-cmin -i afl_in -o afl_out -m none -- cxxfilt"
    dedup_cmd = "afl-cmin -i %s -o %s -m none -- %s" % (input_path, output_path, program_path)
    print(dedup_cmd)
    dedup_pipe = os.popen(dedup_cmd)
    dedup_pipe.read()
    dedup_pipe.close()

def run_zzuf_subprocess(core_index,test_path,program_path, seed_path):
    
    init_process(core_index, "%s/outcomes-%d" % (test_path, core_index))
    
    while True:
         for i in range(100):
             seed_index = random.randint(0,sys.maxsize)
             fuzzing_process(core_index, seed_index, test_path, program_path, seed_path, i)
         print("#%s --- Fuzzing 100 done" % core_index)    
         de_dup_process(core_index, program_path, "%s/outcomes-%d/output" % (test_path, core_index), "%s/outcomes-%d/input" % (test_path, core_index))
         print("#%s --- Deduping 100 done" % core_index)
    #testing_process(core_index, "%s/outcomes-%d/input" % (test_path, core_index),"%s/outcomes-%d/err" % (test_path, core_index), program_path)
    #print("#%s --- Testing 100 done" % core_index)

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
        