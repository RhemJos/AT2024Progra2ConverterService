#
# @Validator.py Copyright (c) 2021 Jalasoft.
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


class Validator(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.splitext(os.path.basename(file_path))[0]
