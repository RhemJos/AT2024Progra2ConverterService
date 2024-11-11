import ffmpeg
import os
from converters.converter import Converter

class VideoConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def to_frames(self, output_path=None, fps=1):
        """Convierte el video en una serie de fotogramas."""
        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', self.filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, '%04d.jpg')

        # Comando ffmpeg para extraer los fotogramas del video
        ffmpeg.input(self.file_path).filter('fps', fps=fps).output(output_path).run(overwrite_output=True)
        return frames_folder

    def to_format(self, output_format=None, fps=None, video_codec=None, audio_codec=None, audio_channels=None):
        """Convierte el video al formato especificado con opciones."""
        input_format = os.path.splitext(self.file_path)[1][1:].lower()
        temp_output_path = os.path.join('outputs', 'video_to_video_outputs', f"{self.filename}-converted.{output_format}")
        output_path = os.path.join('outputs', 'video_to_video_outputs', f"{self.filename}.{output_format}")

        

        # Construcción del comando ffmpeg con los parámetros opcionales
        ffmpeg_command = ffmpeg.input(self.file_path).output(
            temp_output_path if input_format == output_format else output_path,
            **({'vcodec': video_codec} if video_codec else {}),
            **({'acodec': audio_codec} if audio_codec else {}),
            **({'ac': audio_channels} if audio_channels else {}),
            **({'r': fps} if fps else {})
        )

        ffmpeg_command.run(overwrite_output=True)

        # Renombrado del archivo temporal al final si el formato de entrada y salida son iguales
        if input_format == output_format:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_output_path, output_path)

        return output_path
