#
# @audio_options.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
class AudioOptions:
    def __init__(self):
        pass

    # Build options
    @staticmethod
    def build_options_audio(**kwargs) -> dict:
        options = {'vn': None}
        if 'bit_rate' in kwargs:
            options['b:a'] = kwargs['bit_rate']
        if 'channels' in kwargs:
            options['ac'] = kwargs['channels']
        if 'sample_rate' in kwargs:
            options['ar'] = kwargs['sample_rate']
        if 'volume' in kwargs:
            options['af'] = f"volume={kwargs['volume']}"
        if 'language_channel' in kwargs:
            options['map'] = f"0:a:{kwargs['language_channel']}"
        if 'speed' in kwargs:
            speed = float(kwargs['speed'])
            if 'af' in options:
                options['af'] += f",atempo={speed}"
            else:
                options['af'] = f"atempo={speed}"
        return options
