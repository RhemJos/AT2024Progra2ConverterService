#
# @converter.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from abc import ABC, abstractmethod
import os


class Converter(ABC):
    def __init__(self, file_path):  # Constructor to initialize the class with a file path
        self.file_path = file_path  # Store the path of the file to be converted
        self.filename = os.path.splitext(os.path.basename(file_path))[0]  # Extract file name without extension
        self.extension = file_path.split('.')[-1].lower()  # Extract and normalize the file extension (lowercase)
    
    @abstractmethod
    def convert(self, output_format=None, **kwargs):  # Abstract method that must be implemented by subclasses
        """General conversion method. Subclasses must implement it."""
        pass

