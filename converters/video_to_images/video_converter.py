import os
import ffmpeg
from converters.converter import Converter

class VideoConverter(Converter):
    def to_frames(self, output_path=None, fps=1):
        filename = os.path.splitext(os.path.basename(self.file_path))[0] #Obtiene el nombre del video
        frames_folder = os.path.join('outputs', 'video_to_frames_output', filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, 'frame_%d.jpg')
        
        (
            ffmpeg
            .input(self.file_path)
            .filter('fps', fps=fps)
            .output(output_path)
            .run(overwrite_output=True)
        )



    def convert_format(self, output_format=None, output_path=None):
        base_name = os.path.basename(self.file_path)  # Obtiene el nombre base del video con la extensión E.g: .mp4
        file_name = os.path.splitext(base_name)[0]      #Obtiene el nombre del video sin la extensión
        video_path = f'{file_name}.{output_format}'   #Añadiendo nueva extension de video al nombre del video original del input
        video_converted_folder = os.path.join('outputs', 'video_converted_output')
        os.makedirs(video_converted_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(video_converted_folder, video_path)
        print('output_path: ', output_path)
        (
            ffmpeg
            .input(self.file_path)
            .output(output_path)
            .run(overwrite_output=True)
        )

