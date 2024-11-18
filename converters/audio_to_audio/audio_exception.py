#
# @audio_exception.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
class AudioConversionError(Exception):
    # Exception for audio conversion errors
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def get_status_code(self):
        return self.status_code

    def get_message(self):
        return self.message
