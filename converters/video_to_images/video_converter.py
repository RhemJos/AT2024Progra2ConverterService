import os
import ffmpeg

class VideoConverter:
    def __init__(self, video_path):
        self.video_path = video_path

    def to_frames(self, output_path=None, fps=1):
        filename = os.path.splitext(os.path.basename(self.video_path))[0] #Obtiene el nombre del video
        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, 'frame_%04d.jpg')

    def to_format(self, output_format=None, fps=None, video_codec=None, audio_codec=None, audio_channels=None): 
        filename = os.path.splitext(os.path.basename(self.video_path))[0]
        input_format = os.path.splitext(self.video_path)[1][1:].lower()

        temp_output_path = os.path.join('outputs', 'video_to_video_outputs', f"{filename}-converted.{output_format}") # path temporal
        output_path = os.path.join('outputs', 'video_to_video_outputs', f"{filename}.{output_format}")

        ffmpeg_command = ffmpeg.input(self.video_path).output(
            temp_output_path if input_format == output_format else output_path,
            **({'vcodec': video_codec} if video_codec else {}),
            **({'acodec': audio_codec} if audio_codec else {}),
            **({'ac': audio_channels} if audio_channels else {}),
            **({'r': fps} if fps else {})
        )

        ffmpeg_command.run(overwrite_output=True)

        if input_format == output_format:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_output_path, output_path)
