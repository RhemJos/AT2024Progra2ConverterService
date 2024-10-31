import subprocess
import os

class AudioConverter():
    def __init__(self,in_audio):
        self.in_audio=in_audio

    def convert(self,format='mp3',bit_rate=None,channels=None,frecuencia_muestreo=None,volumen=None):
        out_audio = os.path.splitext(self.in_audio)[0]+'.'+format
        # si el archivo ya existe no convertir
        if os.path.exists(out_audio):
            print(f'El archivo {out_audio} ya existe.')
            return out_audio
        # setear opciones
        options = ['-vn'] # opcion para no procesar el stream de video
        if bit_rate:
            options.append(f'-b:a {bit_rate}')
        if channels:
            options.append(f'-ac {channels}')
        if frecuencia_muestreo:
            options.append(f'-ar {frecuencia_muestreo}')
        if volumen:
            options.append(f'-filter:a "volume={volumen}"')

        binary='C:/Users/JoannaPC/ffmpeg/bin/ffmpeg.exe'
        cmd = f'{binary} -n -i {self.in_audio} {" ".join(options)} {out_audio}'
        try:
            result=subprocess.run(cmd, shell=True,check=True,capture_output=True,text=True)
            return out_audio
        except subprocess.CalledProcessError as e:
            print(f"No se pudo convertir el archivo: {e.stderr}")

