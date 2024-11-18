import subprocess
import os
import errno
from exceptions.cmd_execute_exception import CmdExecutionError


class CommandExecutor:
    def get_execfile_path(self, relative_path):
        base_dir = os.getcwd() #Obtiene la ruta base del proyecto
        absolute_file_path = os.path.join( base_dir, relative_path)
        if not os.path.isfile(absolute_file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), absolute_file_path) #Levanta una excepcion en caso de no hallar el archivo
        return absolute_file_path

    def run_command(self, command):
        try:
            return subprocess.run(command, shell=True, check=True, 
                                  encoding='utf-8', capture_output=True).stdout
        except subprocess.CalledProcessError as e:
            raise CmdExecutionError(f"Command {command} execution failed: {e.stderr.decode()}", 500)
        
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


    #Returns a dict containing all needed arguments for a function. 
    #Ensures all arguments are present in the args returned dict. 
    #In case the arg already existed in func_args the values are ketp, otherwise
    #the arg gets added with a default value determined in the parameters definition
    # Parameters -> {"parameter_name" : default_value, ...}
    # Func_args -> kwargs
def get_args(parameters, func_args):
    args = {}
    for parameter_definition in parameters:
        args[parameter_definition] = func_args[parameter_definition] if parameter_definition in func_args else parameters[parameter_definition]
    return args