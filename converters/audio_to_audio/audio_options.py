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
    def __init__(self):  # Initialize the class
        pass

    # Build audio processing options based on input arguments
    @staticmethod
    def build_options_audio(**kwargs) -> dict:
        options = {'vn': None}  # Initialize options with 'vn' key (no video)
        if 'bit_rate' in kwargs:  # Set bit rate if provided
            options['b:a'] = kwargs['bit_rate']
        if 'channels' in kwargs:  # Set number of channels if provided
            options['ac'] = kwargs['channels']
        if 'sample_rate' in kwargs:  # Set sample rate if provided
            options['ar'] = kwargs['sample_rate']
        if 'volume' in kwargs:  # Set volume if provided
            options['af'] = f"volume={kwargs['volume']}"
        if 'language_channel' in kwargs:  # Set language channel if provided
            options['map'] = f"0:a:{kwargs['language_channel']}"
        if 'speed' in kwargs:  # Set speed if provided and within valid range
            speed = float(kwargs['speed'])
            if 0.5 <= speed <= 2.0:
                if 'af' in options:
                    options['af'] += f",atempo={speed}"
                else:
                    options['af'] = f"atempo={speed}"
            else:
                print("Speed must be between 0.5x and 2.0x")
                return None
        return options  # Return the final options dictionary
