from abc import ABC, abstractmethod


class Converter(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
    
    @abstractmethod
    def convert(self):
        ''' Implement convert method '''