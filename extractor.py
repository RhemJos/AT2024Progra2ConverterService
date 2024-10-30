from abc import ABC, abstractmethod


class Extractor(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
    
    @abstractmethod
    def extract(self):
        pass