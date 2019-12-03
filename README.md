# Fuzzing automation tool

## Description:
The tool is an automation tool for running a fuzzer, testing a program and keeping record of the invalid inputs that can crash the program.
At this moment, we support three fuzzers: afl, zzuf and radamsa.
After fuzzing, the tool provides a method for testing crash inputs on different commits of the tested program and recording the results.

## HOW TO:
1. Config files should be placed under the config/ directory. 
2. Enter the directory fuzzing/, run the script *run_fuzzer.py*. e.g., python run_fuzzer.py configfile
3. Results will be stored under your test directory: test_path/outputs-*/err.
4. Before running the tool, the test path you provide should not contain old results.
5. After fuzzing, run the script *map_inputs.py* to generate mapping from inputs to commits, analyze how later commits work on fuzzer generated crash inputs.

## More information on the config file.

In the config file, empty lines are not allowed and the file should be ended with a space.

** An example for fuzzing config files: **

```
fuzzer name = zzuf //Specify which fuzzer to run.

lower = 1 //Assign the core to work. Lower index.

upper = 5 // Upper index.

test path = /home/*/12h-cxxfilt-zzuf // Select a directory to store results

program path = /home/*/binutils_gdb/Benchmark_script/program_files/1/binutils/cxxfilt // The path of the tested program.

seed path = /home/*/12h-cxxfilt-zzuf/seed/emptyseed // The seed file should be provided for fuzzing.

timeout = 86400  //zzuf and radamsa support only numbers in seconds, afl supports 10s, 1m, 2h.
```

For radamsa, the mutation number of each fuzzing should be provided.

For afl, an addtional parameter "afl target option" should be provide.

** Mapping process config file example: **

```
program path = /home/demideng/tool/ins-mapping  *It's the directory that contains all commits to be tested.*

commits file path = /home/demideng/tool/ins-mapping/documents/commits *All commits numbers are stored in the commits file.*

fuzzing output path = /home/demideng/1h-cxxfilt-radamsa *It's the path that stores fuzzing results.*

run command = binutils/cxxfilt < *cmd line for running test of the program.*

output table path = /home/demideng/1h-cxxfilt-radamsa-overlap 

pickle path = /home/demideng/tool/ins-mapping/all_inputs.pickle *All inputs are stored as a pickle.*

```


** Contact: **
demidengonly@gmail.com
