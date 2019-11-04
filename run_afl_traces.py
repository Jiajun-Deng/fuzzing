import os
import multiprocessing
import datetime
import utils.Operations.Operations as op

'''
This tool runs AFL with multiprocessing on given program
This tool uses config options:
  afl output path
  afl program path
  afl target relative path
  afl target option
'''

def run_afl(indexlist, cores, timeout, test_path, program_path,seed_path, afl_target_option):
    pool= multiprocessing.Pool(cores)
    pool.map(run_afl_subprocess, (indexlist, timeout, test_path, program_path,seed_path, afl_target_option))
    pool.close()
    pool.join()
    return

def run_afl_subprocess(core_index,timeout, test_path, program_path,seed_path, afl_target_option):

    afl_output_path = "%s/afl_outcomes_%d" % (test_path ,core_index)
    
    op.mkdir(afl_output_path)
    
    arg = "AFL_USE_ASAN=1 timeout %s afl-fuzz -m none -i %s -o %s %s %s" % (timeout, seed_path, afl_output_path, program_path, afl_target_option)
    print(arg)

    #Record the start time of a process
    with open("%s/start_time_%d" % (afl_output_path, core_index), "w+") as st:
        st.write(str(datetime.datetime.now()))
        
    afl_pipe = os.popen(arg)
    afl_pipe.read()
    afl_pipe.close()
    print("AFL run #%d has ended" % core_index)

def parallel_run_afl (indexlist, cores, timeout, test_path, program_path,seed_path, afl_target_option):
    pool= multiprocessing.Pool(cores)
    try:
        for i in indexlist:
            pool.apply_async(func = run_afl_subprocess, args = (i,timeout, test_path, program_path,seed_path, afl_target_option,))
    except Exception as e:
        print(e)
    pool.close()
    pool.join()