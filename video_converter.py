import ffmpeg


class VideoConverter:
    def __init__(self, video_path):
        self.video_path = video_path

    def to_frames(self, output_path = 'frames/frame_%d.jpg', fps = 1):
        (
            ffmpeg
            .input(self.video_path)
            .filter('fps', fps=fps)
            .output(output_path)
            .run(overwrite_output=True)
        )

    def convert_format(self, output_format =  None):
        base_name = self.video_path.rsplit('.')[0] #Obtener dirección video original sin la extensión
        output_path = f'{base_name}_converted.{output_format}'

        (
            ffmpeg
            .input(self.video_path)
            .output(output_path)
            .run(overwrite_output=True)
        )
