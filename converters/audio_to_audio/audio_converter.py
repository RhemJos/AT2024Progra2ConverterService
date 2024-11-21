#
# @audio_converter.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import os
import ffmpeg
from converters.converter import Converter
from exceptions.audio_convert_exception import AudioConvertError
from converters.audio_to_audio.audio_options import AudioOptions
from validators.format_validator import FormatValidator
from validators.float_validator import FloatValidator
from validators.range_validator import RangeValidator
from validators.len_validator import LenValidator
from validators.validator_context import ValidatorContext
from converters.constants import AUDIO_OPTIONS


class AudioConverter(Converter):
    def __init__(self, audio_path):
        self.audio_path = audio_path
        super().__init__(audio_path)

    def convert(self, **kwargs):
        #Validate parameters
        self.validate_params(**kwargs)

        output_format = kwargs.get("output_format")
        output_path = self._get_output_path(output_format)
        temp_output_path = self._get_temp_output_path(output_format)

        # Get the options
        options = self._get_audio_options(**kwargs)

        self._convert_audio(
            output_path, temp_output_path, output_format, options)
        return temp_output_path if self.extension == output_format else output_path

    def validate_params(self, **kwargs):
        output_format = kwargs.get('output_format')
        validators = [ FormatValidator(output_format, AUDIO_OPTIONS['format'], "Output format") ]
        kwargs = { key: value for key, value in kwargs.items() if value is not None}
        if 'bit_rate' in kwargs:
            validators.append(FormatValidator(kwargs['bit_rate'], AUDIO_OPTIONS['bit_rate'], "Bit rate") )
        if 'channels' in kwargs:
            validators.append(FormatValidator(kwargs['channels'], AUDIO_OPTIONS['audio_channels'], "Audio channels") )
        if 'sample_rate' in kwargs:
            validators.append(FormatValidator(kwargs['sample_rate'], AUDIO_OPTIONS['sample_rate'], "Sample rate") )
        if 'volume' in kwargs:
            validators.append(FormatValidator(kwargs['volume'], AUDIO_OPTIONS['volume'], "Volume") )
        if 'speed' in kwargs:
            validators.append(FloatValidator(kwargs['speed'], True, "Speed") )
            validators.append(RangeValidator(kwargs['speed'], 
                                             AUDIO_OPTIONS['speed_minimum'], AUDIO_OPTIONS['speed_maximum'], "Speed") )
        if "language_channel" in kwargs:
            audio_streams = self._get_audio_streams()
            validators.append(LenValidator(audio_streams, kwargs['language_channel'], 'Language channel' ))
        
        validator_context = ValidatorContext(validators, AudioConvertError)
        validator_context.run_validations()

    
    def _get_output_path(self, output_format):
        # Generate output path for the converted file and change format
        output_file = os.path.splitext(os.path.basename(self.audio_path))[0] + '.' + output_format

        return os.path.join('outputs', 'audio_converted_outputs', output_file)

    def _get_temp_output_path(self, output_format):
        # Generate output path for the converted file and change format
        output_file = os.path.splitext(os.path.basename(self.audio_path))[0] + '_convert.' + output_format

        return os.path.join('outputs', 'audio_converted_outputs', output_file)

    def _convert_audio(self, output_path, temp_output_path, output_format, options):
        # Performs audio conversion using ffmpeg
        try:
            ffmpeg.input(self.audio_path).output(temp_output_path if self.extension ==
                                             output_format else output_path, **options).run(overwrite_output=True)
        except ffmpeg.Error as e:
            raise AudioConvertError(f"Ffmpeg command for audio convertion failed: {e}", 500)

    def _get_audio_options(self, **kwargs):
        # Verifies that options have been built
        opt = AudioOptions.build_options_audio(**kwargs)
        return opt
    
    def _get_audio_streams(self):
        # Extracts the audio streams
        try:
            result = ffmpeg.probe(self.audio_path, cmd='ffprobe', **{ "select_streams": "a"})
        except ffmpeg.Error as e:
            raise AudioConvertError(f"Ffmpeg command for for validating audio streams failed: {e}", 500)
        return result["streams"]
