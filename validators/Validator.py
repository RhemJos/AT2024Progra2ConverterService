from abc import ABC, abstractmethod
import os


class Validator(ABC):
    def __init__(self, options, error_class):
        self.options = options
        self.error_class = error_class
        
    def validate_format(self, entered_format, reference_format, param_name):
        if entered_format not in self.options[reference_format]:  # Obligatorio
            raise self.error_class(f"{param_name}: '{entered_format}' no es válido. Opciones válidas: {self.options[reference_format]}.", 400)

    def validate_int(self, number, param_name):
        try:
            int(number)
        except ValueError:
            raise self.error_class(f"{param_name} debe ser un número entero.", 400)
        
    @abstractmethod
    def validate(self, **kwargs):
        pass

