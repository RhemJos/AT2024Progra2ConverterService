import ffmpeg
import os
from converters.converter import Converter


class VideoToImagesConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, output_path=None, fps=1):
        # Convierte el video en una serie de fotogramas
        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', self.filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, '%d.jpg')

        # Comando ffmpeg para extraer los fotogramas del video
        ffmpeg.input(self.file_path).filter('fps', fps=fps).output(output_path).run(overwrite_output=True)
        return frames_folder
