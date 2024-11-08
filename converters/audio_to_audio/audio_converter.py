import os
import ffmpeg

from converters.audio_to_audio.audio_options import AudioOptions


class AudioConverter():
    def __init__(self,audio_path):
        self.audio_path=audio_path

    def convert(self, output_format='mp3', **kwargs):
        output_file = os.path.splitext(os.path.basename(self.audio_path))[0] +'.' + output_format
        output_path = os.path.join('outputs','audio_converted_outputs',output_file)

        # si el archivo ya existe no convertir
        if os.path.exists(output_path):
            print(f'El archivo {output_path} ya existe.')
            return output_path

        # setear opciones
        builder_options = AudioOptions()
        options = builder_options.build_options_audio(**kwargs)
        if options is None:
            return None #cambiar a excepcion en vez de return none

        try:
            stdout,stderr=(
                ffmpeg
                .input(self.audio_path)
                .output(output_path,
                        **options
                        )
                #.run(overwrite_output=True)
                .run(capture_stdout=True,capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print(f"Algo falló en la conversión : {e.stderr.decode()}")
        else:
            return output_path
