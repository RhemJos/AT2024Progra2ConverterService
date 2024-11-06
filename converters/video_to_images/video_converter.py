import os
import ffmpeg

class VideoConverter:
    def __init__(self, video_path):
        self.video_path = video_path

    def to_frames(self, output_path=None, fps=1):
        filename = os.path.splitext(os.path.basename(self.video_path))[0] #Obtiene el nombre del video
        frames_folder = os.path.join('outputs', 'video_to_frames_output', filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, 'frame_%d.jpg')
        
        (
            ffmpeg
            .input(self.video_path)
            .filter('fps', fps=fps)
            .output(output_path)
            .run(overwrite_output=True)
        )



    def convert_format(self, output_format=None, output_path=None):
        base_name = os.path.basename(self.video_path)  # Obtiene el nombre base del video con la extensión E.g: .mp4
        file_name = os.path.splitext(base_name)[0]      #Obtiene el nombre del video sin la extensión
        video_path = f'{file_name}.{output_format}'   #Añadiendo nueva extension de video al nombre del video original del input
        video_converted_folder = os.path.join('outputs', 'video_converted_output')
        os.makedirs(video_converted_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(video_converted_folder, video_path)
        print('output_path: ', output_path)
        (
            ffmpeg
            .input(self.video_path)
            .output(output_path)
            .run(overwrite_output=True)
        )

    def convert_to_mov_with_fps(self, output_path=None, fps=24, codec="libx264"):
        """
        Convierte el video a formato MOV y ajusta los fotogramas por segundo (fps) para reducir el tamaño.
        
        :param codec: Códec a utilizar para la compresión del video. Por defecto es libx264.
        """
        base_name = os.path.basename(self.video_path)
        file_name = os.path.splitext(base_name)[0]
        video_converted_folder = os.path.join('outputs', 'mov_videos')
        os.makedirs(video_converted_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(video_converted_folder, f"{file_name}.mov")

        (
            ffmpeg
            .input(self.video_path)
            .output(output_path, vcodec=codec, r=fps)  # vcodec define el codec de video, r establece el FPS
            .run(overwrite_output=True)
        )
        print(f"Video convertido a MOV con {fps} fps en la ruta: {output_path}")