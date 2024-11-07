import os
import ffmpeg

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
        options= {'vn':None}
        if 'bit_rate' in kwargs:
            options['b:a']= kwargs['bit_rate']
        if 'channels' in kwargs:
            options['ac']= kwargs['channels']
        if 'sample_rate' in kwargs:
            options['ar']= kwargs['sample_rate']
        if 'volume' in kwargs:
            options['af']= f"volume={kwargs['volume']}"
        if 'language_channel' in kwargs:
            options['map'] = f'0:a:{kwargs["language_channel"]}'

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
