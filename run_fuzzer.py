import run_radamsa_traces as ra
import run_afl_traces as rafl

from utils.Config.Config import Config
from utils.GetFunctions.GetFunctions import get_range

     
if __name__ == "__main__":
  
  fuzzer_name = input("Choose the fuzzer: afl, radamsa, zzuf:")
  
  if fuzzer_name == "radamsa":
      print("Fuzzing and testing of radamsa begins:")
      
      lower, upper = get_range()
      config = Config()
      index_list = list(range(lower,upper))#Decide which cores to use.
      
      #global variable is used by all processes.
      global timeout
      timeout = config.get_config("timeout")
      timeout = int(timeout)
      
      global fuzzer_path
      fuzzer_path = config.get_config("fuzzer_path")
      
      global seed_path
      seed_path = config.get_config("seed_path")
      
      global test_path
      test_path = config.get_config("test_path")
      output_path = "%s/out" % (test_path)
      err_path = "%s/err" % (test_path)
      
      global mutation_num
      mutation_num = config.get_config("mutation_num")
      mutation_num = int(mutation_num)
    
      global program_path
      program_path = config.get_config("program_path")
      
      ra.parallel_run_radamsa_with_timeout(index_list, upper-lower+1, test_path, program_path, fuzzer_path, seed_path, mutation_num, timeout)
      
  elif fuzzer_name == "afl":
  
    lower, upper = get_range()
    
    config = Config()
        
    indexlist = list(range(lower, upper+1))

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

    rafl.run_afl(indexlist, upper-lower+1)

      
  elif fuzzer_name == "zzuf":
      print("TODO")
  else:
      print("TODO MORE FUZZERS")