import cv2
import os
from moviepy.editor import VideoFileClip


class VideoConverter:
    def __init__(self, video_path):
        self.video_path = video_path

    def to_frames(self, output_path=None, fps=1):
        filename = os.path.splitext(os.path.basename(self.video_path))[0]  # Obtiene el nombre del video
        frames_folder = os.path.join('outputs', 'video_to_frames_output', filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            # output_path = os.path.join(frames_folder, 'frame_%04d.jpg')
            output_path = frames_folder

        load_video = cv2.VideoCapture(self.video_path)
        original_fps = load_video.get(cv2.CAP_PROP_FPS)
        frame_interval = int(original_fps // fps) if fps > 0 else 1

        # Contador de frames
        frame_number = 0
        saved_frames = 0

        while True:
            ret, frame = load_video.read()
            if not ret:
                break  # Termina cuando ya no hay más frames

            # Guardar solo cada "frame_interval" frames
            if frame_number % frame_interval == 0:
                # Nombre del archivo del frame
                frame_filename = os.path.join(output_path, f"frame_{saved_frames:04d}.jpg")
                print(frame_filename)
                # Guardar el frame como imagen
                cv2.imwrite(frame_filename, frame)
                saved_frames += 1

            # Incrementar el contador de frames
            frame_number += 1

        # Liberar el objeto VideoCapture
        load_video.release()

    def convert_format(self, output_format=None, output_path=None):
        base_name = os.path.basename(self.video_path)  # Obtiene el nombre base del video con la extensión (e.g., .mp4)
        file_name = os.path.splitext(base_name)[0]  # Obtiene el nombre del video sin la extensión
        video_path = f'{file_name}.{output_format}'  # Nueva extensión para el video
        print(video_path)
        video_converted_folder = os.path.join('outputs', 'video_converted_output')
        os.makedirs(video_converted_folder, exist_ok=True)

        # Definir el output_path si no se especifica
        if output_path is None:
            output_path = os.path.join(video_converted_folder, video_path)

        # Convertir el video
        with VideoFileClip(self.video_path) as video_clip:
            video_clip.write_videofile(output_path,
                                       codec='libx264')

        return output_path
