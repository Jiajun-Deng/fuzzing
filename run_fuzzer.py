import run_radamsa_traces as ra
import run_afl_traces as rafl
import run_zzuf_traces as rz

from utils.Config.Config import Config
from utils.GetFunctions.GetFunctions import get_range

     
if __name__ == "__main__":
    
    config = Config()
    
    global fuzzer_name
    fuzzer_name = config.get_config("fuzzer name")
    
    global timeout
    timeout = config.get_config("timeout")    
    
    global lower
    lower = config.get_config("lower")
    lower = int(lower)
    
    global upper
    upper = config.get_config("upper")
    upper = int(upper)
    index_list = list(range(lower,upper+1))#Decide which cores to use.
     
    global test_path
    test_path = config.get_config("test path")
    
    global program_path
    program_path = config.get_config("program path")

    global seed_path
    seed_path = config.get_config("seed path")
    
    if fuzzer_name == "radamsa":
        print("Fuzzing and testing of radamsa begins:")

        timeout = int(timeout)
        
        global fuzzer_path
        fuzzer_path = config.get_config("fuzzer path")
        
        output_path = "%s/out" % (test_path)
        err_path = "%s/err" % (test_path)
        
        global mutation_num
        mutation_num = config.get_config("mutation num")
        mutation_num = int(mutation_num)

        ra.parallel_run_radamsa_with_timeout(index_list, upper-lower+1, test_path, program_path, fuzzer_path, seed_path, mutation_num, timeout)
      
    elif fuzzer_name == "afl":
    
        global afl_target_option
        afl_target_option = config.get_afl_target_option()
    
        rafl.parallel_run_afl(index_list, upper-lower+1, timeout, test_path, program_path,seed_path, afl_target_option)

      
    elif fuzzer_name == "zzuf":

        timeout = int(timeout)
        
        rz.parallel_run_zzuf_with_timeout(index_list, upper-lower+1, test_path, program_path,seed_path, timeout)
        
    else:
        print("TODO MORE FUZZERS")