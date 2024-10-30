import subprocess

class AudioConverter():
    def __init__(self,in_audio):
        self.in_audio=in_audio

    def set_out_audio(self,out_format):
        out_audio=self.in_audio.split('.')[0]+'.'+out_format
        return out_audio

    def convert(self,format='mp3',bit_rate=None,channels=None):
        options = ['-vn'] # opcion para no procesar el stream de video
        if bit_rate:
            options.append(f'-b:a {bit_rate}')
        if channels:
            options.append(f'-ac {channels}')
        out_audio=self.set_out_audio(format)
        binary='C:/Users/JoannaPC/ffmpeg/bin/ffmpeg.exe'
        cmd = f'{binary} -n -i {self.in_audio} {" ".join(options)} {out_audio}'
        # return(cmd)
        try:
            subprocess.check_output(cmd, shell=True)
            return out_audio
        ## buscar una manera de capturar los errores y si el archivo ya existe devolver el nombre del archivo
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit status {e.returncode}")
            print(f"Output: {e.output.decode()}")
