#
# @extractor.py Copyright (c) 2021 Jalasoft.
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


class Extractor(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
    
    @abstractmethod
    def extract(self):
        ''' Implement extraction method '''
