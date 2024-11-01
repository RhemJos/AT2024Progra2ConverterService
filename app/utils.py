import subprocess
import os


class CommandExecutor:
    def get_execfile_path(self, relative_path):
        return os.getcwd() + relative_path

    def run_command(self, command):
        try:
            return subprocess.run(command, shell=True, check=True, 
                                  encoding='utf-8', capture_output=True).stdout
        except subprocess.CalledProcessError:
            return "No se pudo ejecutar el comando"
        
class Formatter:
    # Formats a string containing key:value pairs into a dictionary
    def key_value_string_to_dict(self, text, key_value_divider, pairs_divider):
        key_value_pairs = text.split(pairs_divider)
        dict = {}
        for pair in key_value_pairs:
            divided_pair = pair.split(key_value_divider, 1)
            if len(divided_pair) == 2:
                dict[divided_pair[0]] = divided_pair[1]
        return dict


