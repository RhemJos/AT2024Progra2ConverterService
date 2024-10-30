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
