import os, signal
import multiprocessing
import subprocess

'''
Wrapper for run_radamsa_subprocess, can kill a process after timeout.
Timeout is implemented as an alarm.
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
def parallel_run_fuzzer_with_timeout (indexlist, cores, test_path, program_path, seed_path, timeout):
    pool= multiprocessing.Pool(cores)
    try:
        for i in indexlist:
            pool.apply_async(func = run_fuzzer_with_alarm, args = (i,test_path, program_path, seed_path, timeout,))
    except Exception as e:
        print(e)
    pool.close()
    pool.join()