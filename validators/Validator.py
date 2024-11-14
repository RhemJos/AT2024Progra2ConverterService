from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, param_name):
        self.error_class = Exception()
        self.param_name = param_name
        
    @abstractmethod
    def validate(self):
        pass

    def set_error_class(self, error_class):
        self.error_class = error_class

