import ffmpeg
import os
from converters.converter import Converter
from validators.VideoValidator import VideoValidator
from exceptions.video_convert_exception import VideoConvertError
from utils import get_args

class VideoToVideoConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, output_format=None, **kwargs):
        input_format = os.path.splitext(self.file_path)[1][1:].lower()
        temp_output_path = os.path.join('outputs', 'video_to_video_outputs', f"{self.filename}-converted.{output_format}")
        output_path = os.path.join('outputs', 'video_to_video_outputs', f"{self.filename}.{output_format}")

        # Inicializar comando ffmpeg con entrada
        ffmpeg_command = ffmpeg.input(self.file_path)

        # Agregar parámetros opcionales a la salida
        output_args = {}
        if 'fps' in kwargs and kwargs['fps']:
            output_args['r'] = int(kwargs['fps'])
        if 'video_codec' in kwargs and kwargs['video_codec']:
            output_args['vcodec'] = kwargs['video_codec']
        if 'audio_codec' in kwargs and kwargs['audio_codec']:
            output_args['acodec'] = kwargs['audio_codec']
        if 'audio_channels' in kwargs and kwargs['audio_channels']:
            output_args['ac'] = int(kwargs['audio_channels'])
        
        # Validación de parámetros
        validation_errors = VideoValidator.validate(output_format=output_format, **output_args)
        if validation_errors:
            raise VideoConvertError( str(validation_errors), 400 )

        # Construcción del comando ffmpeg con los parámetros opcionales en una sola salida
        ffmpeg_command = ffmpeg_command.output(temp_output_path if input_format == output_format else output_path, **output_args)

        try:
            # Ejecución del comando ffmpeg
            ffmpeg_command.run(overwrite_output=True)

            # Renombrado del archivo temporal si los formatos coinciden
            if input_format == output_format:
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(temp_output_path, output_path)

            return output_path

        except ffmpeg.Error as e:
            print(f"Error al ejecutar el comando ffmpeg: {e.stderr.decode('utf8')}")
            raise
