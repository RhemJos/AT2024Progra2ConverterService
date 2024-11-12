import ffmpeg
import os
from converters.converter import Converter


class VideoToImagesConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, output_path=None, **kwargs):
        # Extraemos el valor de fps de kwargs, o usamos 1 como valor por defecto
        fps = kwargs.get('fps', 1)

        # Convierte el video en una serie de fotogramas
        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', self.filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, '%d.jpg')

        # Comando ffmpeg para extraer los fotogramas
        ffmpeg_command = ffmpeg.input(self.file_path)

        # Aplicar el filtro fps en la entrada
        ffmpeg_command = ffmpeg_command.filter('fps', fps=fps)

        # Definir la salida del comando
        ffmpeg_command = ffmpeg_command.output(output_path)

        try:
            # Ejecutar el comando ffmpeg
            ffmpeg_command.run(overwrite_output=True)
            return frames_folder
        except ffmpeg.Error as e:
            # Capturar y mostrar el error si ocurre
            if e.stderr:
                print(f"Error al ejecutar el comando ffmpeg: {e.stderr.decode('utf8')}")
            else:
                print("Error desconocido al ejecutar el comando ffmpeg.")
            raise
