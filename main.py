from audio_converter import AudioConverter

if __name__=='__main__':
    audio_converter = AudioConverter('C:/Users/JoannaPC/Music/NewRules.m4a')
    print(audio_converter.convert(format='ogg',bit_rate='96k',channels=8,frecuencia_muestreo=8000,volumen=0.5))
