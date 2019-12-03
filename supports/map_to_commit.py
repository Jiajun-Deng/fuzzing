import subprocess

'''
This method will write a map_log file by testing crashed inputs on different commits of the tested program.

commits: an object construted from the commits file.
inputs: an object constructed from crashed inputs.
arg: cmd line for testing the program.
program_path: the program commits path.
map_log: a file that will store the input mapping information. Specifically, its information on what inputs crashed now passed.
afl_id: Used to specifiy a fuzzing outcome directory.
'''
def map_to_commit(commits, inputs, arg, program_path, map_log, afl_id):
    inputs_left = inputs
    for commit in commits:
        version_path = "%s/program_files/%s" % (program_path, commit.get_name())

        # a list to store error inputs for current version
        error_inputs = []
        pass_inputs = []
        # if no error inputs left
        if not inputs_left:
            break
        for input in inputs_left:
            args = "%s/%s %s" % (version_path, arg, input.get_path())
            #print(args)
            run_pipe = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = run_pipe.communicate()
            if err:
                error_inputs.append(input)
            else:
                pass_inputs.append(input)
                input.add_mapping(commit.get_index())
        #Collect original-crash-now-pass inputs, meaning fixed bugs.
        if pass_inputs:
            pass_ids = [i.get_id() for i in pass_inputs]
            msg = " ".join(
                ["afl_%d" % afl_id, str(commit.get_index()), commit.get_id(), str(len(pass_ids)), str(pass_ids)])
            map_log.write(msg + "\n")
        # inputs_left = error_inputs


def map_by_timeline(inputs, timeline_log):
    for input in inputs:
        msg = " ".join([str(input.get_id()), str(input.get_mtime()), str(input.get_mapping())])
        timeline_log.write(msg + "\n")
