from validators.validator import Validator
import os

class FileValidator(Validator):
    def __init__(self, path, is_dir : bool, param_name):
        super().__init__( param_name)
        self.path = path
        self.is_dir = is_dir
        
    def validate(self):
        if self.is_dir:
            if not os.path.isdir(self.path):
                raise self.error_class(f"{self.param_name}: {self.path} is not a valid directory", 400)
        else:
            if not os.path.isfile(self.path):
                raise self.error_class(f"{self.param_name}: {self.path} is not a valid file", 400)


