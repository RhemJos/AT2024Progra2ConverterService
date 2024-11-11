from abc import ABC, abstractmethod
import os


class Validator(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.splitext(os.path.basename(file_path))[0]