import ffmpeg
import os
from converters.converter import Converter


class VideoToImagesConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, output_path=None, fps=1, **kwargs):
        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', self.filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, '%d.jpg')

        ffmpeg_command = ffmpeg.input(self.file_path)

        if fps:
            ffmpeg_command = ffmpeg_command.filter('fps', fps=fps)

        ffmpeg_command = ffmpeg_command.output(output_path, **kwargs)

        try:
            ffmpeg_command.run(overwrite_output=True)
            return frames_folder
        except ffmpeg.Error as e:
            print(f"Error al ejecutar el comando ffmpeg: {e.stderr.decode('utf8')}")
            raise
