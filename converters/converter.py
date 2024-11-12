from abc import ABC, abstractmethod
import os


class Converter(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.splitext(os.path.basename(file_path))[0]
        self.extension = file_path.split('.')[-1].lower()
    
    @abstractmethod
    def convert(self, output_format=None, **kwargs):
        """Método general de conversión. Las subclases deben implementarlo."""
        raise NotImplementedError("Este método debe ser implementado por cada convertidor específico")
    
    def get_output_path(self, output_dir, filename, extension):
        os.makedirs(output_dir, exist_ok = True)
        return os.path.join(output_dir, f"{filename}.{extension}")
