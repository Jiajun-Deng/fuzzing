# The tool to run fuzzers automatically.

Requirements:

1.Create a script for running fuzzer(such as radamsa, zzuf and afl) automatically.

2.The script should be able to take the parameter of a fuzzer's name then determine to run the specific fuzzer.

3.At the second level, the tool should be able to take in parameters for a fuzzer from the config file.



Development plan:

1.Understand the requirements.

2.Trial on basic use of fuzzers(afl, libfuzzer, radamsa and zzuf).

3.Experimenting on automation of running radamsa and testing cxxfilt.

4.Refactoring the script code to handle more fuzzers.

5.Debugging.
