import sys


class Config:
    def __init__(self):
        self.config = {}
        if len(sys.argv) > 1:
            setup = sys.argv[1]
        else:
            setup = input("Enter the config file name: ")
        with open("configs/%s" % setup, "r") as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == "#":
                continue
            l = line.split(" = ")
            self.config[l[0]] = l[1][:-1]

    def get_config(self, config_name):
        path = self.config[config_name]
        print("\033[93m%s is %s\x1b[0m" % (config_name, path))
        input("Press Enter to continue...")
        return path

    def get_commits_path(self):
        return self.get_config("commits file path")

    def get_afl_output_path(self):
        return self.get_config("afl output path")

    def get_mapping_result_path(self):
        return self.get_config("mapping result path")

    def get_afl_program_path(self):
        return self.get_config("afl program path")

    def get_afl_target_relative_path(self):
        return self.get_config("afl target relative path")

    def get_afl_target_option(self):
        return self.get_config("afl target option")

    def get_program_path(self):
        return self.get_config("program path")

    def get_run_command(self):
        return self.get_config("run command")

    def get_instrumentation_folder_path(self):
        return self.get_config("instrumentation folder path")

    def get_target_relative_path(self):
        return self.get_config("target relative path")

    def get_output_table_path(self):
        return self.get_config("output table path")

    '''
    def get_before_fix_path(self):
        return self.get_config("before fix path")

    def get_after_fix_path(self):
        return self.get_config("after fix path")

    def get_revert_fix_path(self):
        return self.get_config("revert fix path")

    def get_instrumented_path(self):
        return self.get_config("instrumented path")

    def get_error_inputs_path(self):
        return self.get_config("error inputs path")
    '''
