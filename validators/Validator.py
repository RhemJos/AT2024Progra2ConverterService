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


class Validator(ABC):
    def __init__(self, param_name):
        self.error_class = Exception()
        self.param_name = param_name
        
    @abstractmethod
    def validate(self):
        pass

    def set_error_class(self, error_class):
        self.error_class = error_class

