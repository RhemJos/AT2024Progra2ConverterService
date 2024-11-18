import ffmpeg
import os
from converters.converter import Converter
from validators.format_validator import FormatValidator
from validators.int_validator import IntValidator
from validators.validator_context import ValidatorContext
from exceptions.video_convert_exception import VideoConvertError


VIDEO_OPTIONS = {
            "format": ["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
            "vcodec": ["libx264", "libx265", "mpeg4", "vp8", "vp9", "prores", "huffyuv", "hevc_nvenc"],
            "acodec": ["aac", "mp3", "opus", "ac3", "pcm_s16le", "vorbis"],
            "audio_channels": ['1', '2', '4', '6', '8']
        }

class VideoToVideoConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, **kwargs):
        # Validates params
        self.validate_params( **kwargs)

        output_format = kwargs.get('output_format')
        input_format = os.path.splitext(self.file_path)[1][1:].lower()
        temp_output_path = os.path.join('outputs', 'video_to_video_outputs', f"{self.filename}-converted.{output_format}")
        output_path = os.path.join('outputs', 'video_to_video_outputs', f"{self.filename}.{output_format}")

        # Initilize ffmpeg command
        ffmpeg_command = ffmpeg.input(self.file_path)

        # Adds optional params
        output_args = {}
        if 'fps' in kwargs and kwargs['fps']:
            output_args['r'] = kwargs['fps']
        if 'video_codec' in kwargs and kwargs['video_codec']:
            output_args['vcodec'] = kwargs['video_codec']
        if 'audio_codec' in kwargs and kwargs['audio_codec']:
            output_args['acodec'] = kwargs['audio_codec']
        if 'audio_channels' in kwargs and kwargs['audio_channels']:
            output_args['ac'] = int(kwargs['audio_channels'])

        # Construcción del comando ffmpeg con los parámetros opcionales en una sola salida
        ffmpeg_command = ffmpeg_command.output(temp_output_path, **output_args)

        try:
            ffmpeg_command.run(overwrite_output=True)

            # Renombrado del archivo temporal si los formatos coinciden
            # if input_format == output_format:
                # if os.path.exists(output_path):
                #     # os.remove(output_path)
                # os.rename(temp_output_path, output_path)

            return output_path

        except ffmpeg.Error as e:
            raise VideoConvertError(f"Ffmpeg command execution failed: {e.stderr}" , 500)

    def validate_params(self, **kwargs):
        validators = [ FormatValidator(kwargs['output_format'], VIDEO_OPTIONS['format'], "Output format") ]
    
        if kwargs['fps']:
            validators.append(IntValidator(kwargs['fps'], True, "Frames per second") )
        if kwargs['video_codec']:   
            validators.append(FormatValidator(kwargs['video_codec'], VIDEO_OPTIONS['vcodec'], "Video codec") )
        if kwargs['audio_codec']:
            validators.append(FormatValidator(kwargs['audio_codec'], VIDEO_OPTIONS['acodec'], "Audio codec") )
        if kwargs['audio_channels']:
            validators.append(FormatValidator(kwargs['audio_channels'], VIDEO_OPTIONS['audio_channels'], "Audio channels") )

        validator_context = ValidatorContext(validators, VideoConvertError)
        validator_context.run_validations()

        



