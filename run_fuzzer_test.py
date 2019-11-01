import os
import multiprocessing
import datetime
import shutil
import subprocess

from utils.Config.Config import Config
from utils.GetFunctions.GetFunctions import get_range


'''
indexlist: the list of all cores
cores: the number of cores assigned.
'''
def run_fuzzer(indexlist, cores):
    pool= multiprocessing.Pool(cores)
    pool.map(run_fuzzer_subprocess, indexlist)
    pool.close()
    pool.join()
    return
   
'''
Get the system now time in timestamp.
'''   
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
        #print ("ERROR: "+ path + " already exists.")
        return False
    
    

def run_cmd(cmd):
    
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return p
    
'''
Param: core_index, its default value is 1. It's used to assign a core to run the subprocess.
'''
def run_fuzzer_subprocess(core_index=1):

    #Create a dir for invalid input strings
    invalid_output_path = "%s/outcomes_%d" % (err_path, core_index)
    mkdir(invalid_output_path)
    
    #infinite loop
    while True:
      #Fuzzing
      fuzzer_run_cmd = "%s  -n %d %s" % (fuzzer_path, mutation_num, seed_path)
      #print(fuzzer_run_cmd)
  
      fuzzer_return = run_cmd(fuzzer_run_cmd)
      outs, errs = fuzzer_return.communicate() # outs type: byte
      
      #remove duplicates in outs
      out_bytes = outs.split(b"\n") #b means binary
      out_nondup = set(out_bytes)
      
      index = 0
      
      for output in out_nondup:
          #bytes to string
          #output = output.decode("utf-8")
  
          #Testing cxxfilt
          test_cmd = "%s %s" % (program_path, output)
          print(test_cmd)
          test_return = run_cmd(test_cmd)
          
          test_out, test_err = test_return.communicate()
          
          if test_err:
              index +=1
              print("ERROR %d" % index)
              print(test_err)
              
          #Write err outputs to err directory
              with open("%s/outcomes_%d/id:_%d;timestamp:_%s" % (err_path,core_index, index, get_now_timestamp()), "wb+") as st:  #wb+, open
                  st.write(output)    

'''
main:
1. Read arguments from the config file.
2. Multiprocessing run fuzzer, run testing program, decide the outputs
3. Output file format, name
'''


#Manually check the invalid output:
#/home/zenong/binutils_gdb/Benchmark_script/program_files/1_371517f576f8e7b25fc228c7459d6865c13d524/binutils/cxxfilt < /home/demideng/72h-cxxfilt-radamsa/err/outcomes_3/invalid_output_1

if __name__ == "__main__":

  lower, upper = get_range()
  print("lower = %d" % lower)
  print("upper = %d" % upper)
  
  config = Config()
  
  global timeout
  timeout = config.get_config("timeout")
  print("timeout = %d" % int(timeout))
  
  global fuzzer_path
  fuzzer_path = config.get_config("fuzzer_path")
  print("fuzzer_path = %s" % fuzzer_path)
  
  global seed_path
  seed_path = config.get_config("seed_path")
  print("seed_path = %s" % seed_path)
  
  global test_path
  test_path = config.get_config("test_path")
  #output_path = "%s/out" % (test_path)
  err_path = "%s/err" % (test_path)
  print("test_path = %s" % test_path)
  
  global mutation_num
  mutation_num = config.get_config("mutation_num")
  print("mutation_num = %d" % int(mutation_num))
  
  global program_path
  program_path = config.get_config("program_path")
  print("program_path = %s" % program_path)
  
  #index_list = list(range(1,6))
  
  #run_fuzzer(index_list, 5)
  
'''
TODO: 11-1
How to control the timeout.
A single process to control all the other processes.
Another way: hang on each process within the process itself. wait?

Error: not valid for multiprocessing.

  TIMEOUT = 10

  process = multiprocessing.Process(target=run_fuzzer_subprocess)
  process.daemon = True
  process.start()
  
  process.join(TIMEOUT)
  if process.is_alive():
      print("Function is hanging!")
      process.terminate()
      print("Terminated!") 
'''
