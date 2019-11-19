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
        op.mkdir("%s/err" % work_path)#err_path
        op.mkdir("%s/err_d" % work-path)#err after de-duplicating
'''
Generates mutations to output path using stdin fuzzing mode of zzuf.
cmd line: zzuf -r 0.01:0.9 -s 200 < seedfile  >  output/id_1
The above cmd line generates one mutation file for seed 200.
'''
def fuzzing_process(core_index, test_path, seed_path):
    for i in range(100):
        seed_index = random.randint(0,sys.maxsize)
        fuzzing_arg = "zzuf -r 0.01:0.9 -s %s <%s > %s/outcomes-%d/output/id_%d" % (seed_index, seed_path, test_path, core_index, i)
        fuzzing_return = subprocess.Popen(fuzzing_arg, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
'''
Tests all files under input_path, if an input crashes the tested program, this file will be copied to the err path.
'''
def testing_process(core_index, input_path, err_path, program_path):
    input_files = os.listdir("%s/" % input_path)

    for onefile in input_files:
        test_input = "%s/%s" % (input_path, onefile)
        test_cmd = "%s < %s" % (program_path, test_input)
        test_return = op.run_cmd(test_cmd)
        test_out, test_err = test_return.communicate()
    
        #If the input crashes the program, copy it to err/ dir.
        if test_err:
              print(test_err)
              err_destination = "%s/%s;timestamp_%s" % (err_path, onefile, op.get_now_timestamp())
              op.copyfile(test_input, err_destination)

'''
Remove duplicates using afl-cmin.
cmd line: "afl-cmin -C -i input_dir -o output_dir -m none -- cxxfilt"
afl-cmin can't recognize files generated by zzuf without -C flag.
'''
def de_dup_process(core_index, program_path, input_path, output_path):
    op.rmdir(output_path)
    dedup_cmd = "afl-cmin -C -i %s -o %s -m none -- %s" % (input_path, output_path, program_path)
    dedup_return = subprocess.Popen(dedup_cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out,err = dedup_return.communicate()
    
'''
The subprocess that initilizes the testing directory,
then keeps running fuzzing-testing-deduplicating processes in a sequence.
'''
def run_zzuf_subprocess(core_index,test_path,program_path, seed_path):
    
    init_process(core_index, "%s/outcomes-%d" % (test_path, core_index))
  
    while True:
         fuzzing_process(core_index, test_path, seed_path)
         testing_process(core_index, "%s/outcomes-%d/output" % (test_path, core_index),"%s/outcomes-%d/err" % (test_path, core_index), program_path)
         de_dup_process(core_index, program_path, "%s/outcomes-%d/err" % (test_path, core_index), "%s/outcomes-%d/err_d" % (test_path, core_index))
         
'''
Wrap the subprocess with an alarm for the timeout control.
'''
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
        