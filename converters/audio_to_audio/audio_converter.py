import os
import ffmpeg
from converters.converter import Converter

from exceptions.audio_convert_exception import AudioConvertError
from converters.audio_to_audio.audio_options import AudioOptions
from validators.format_validator import FormatValidator
from validators.float_validator import FloatValidator
from validators.range_validator import RangeValidator
from validators.validator_context import ValidatorContext



AUDIO_OPTIONS = {
            "format": ["mp3", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
            "bit_rate": ["32K", "64K", "96K", "128K", "192K", "256K", "320K"],
            "audio_channels": ['1', '2', '3', '4', '5' ,'6','7' ,'8'],
            "sample_rate": ['8000', '22050' , '44100' , '48000' , '96000', '192000'],
            "volume": ['0.5', '1.5'],
            "speed": [0.5, 2.0] # Range
        }


class AudioConverter(Converter):
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def convert(self, **kwargs):
        #Validate parameters
        self.validate_params(**kwargs)

        output_format = kwargs.get("output_format", 'mp3')
        output_path = self._get_output_path(output_format)

        # If the file already exists do not convert
        if os.path.exists(output_path):
            os.remove(output_path)

        # Set options
        options = self._get_audio_options(**kwargs)

        try:
            self._convert_audio(output_path, options)
        except ffmpeg.Error as e:
            raise AudioConvertError(f"Ffmped command for audio convertion failed: {e.stderr.decode()}", 500)
        else:
            return output_path

    def validate_params(self, **kwargs):
        validators = [ FormatValidator(kwargs['output_format'], AUDIO_OPTIONS['format'], "Output format") ]
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
            validators.append(RangeValidator(kwargs['speed'], 0.5, 2.0, "Speed") )
        
        validator_context = ValidatorContext(validators, AudioConvertError)
        validator_context.run_validations()

    
    def _get_output_path(self, output_format):
        # Generate output path for the converted file and change format
        output_file = os.path.splitext(os.path.basename(self.audio_path))[0] + '.' + output_format
        return os.path.join('outputs', 'audio_converted_outputs', output_file)

    def _convert_audio(self, output_path, options):
        # Performs audio conversion using ffmpeg
        ffmpeg.input(self.audio_path).output(output_path, **options).run(capture_stdout=True, capture_stderr=True)

    def _get_audio_options(self, **kwargs):
        # Verifies that options have been built
        opt = AudioOptions.build_options_audio(**kwargs)
        return opt
    

