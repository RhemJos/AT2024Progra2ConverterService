import os
from audio_converter import AudioConverter


if __name__=='__main__':
    # el nombre de archivo en la carpeta inputs
    input_path = os.path.join('inputs', 'NewRules.m4a')
    audio_converter = AudioConverter(input_path)
    # print(audio_converter.convert(output_format='opus', channels=2, volume=1.5))
    print(audio_converter.convert(output_format='wav', bit_rate='96k', channels=5, sample_rate=8000, volume=0.5))


    # se pueden realizar varias transformaciones al audio, las que escogí son:

    # output_format: la extension del nuevo audio (mp3,ogg,m4a,wav,flac,opus)
    # bit_rate:      refiere a la cantidad de datos procesados por segundo y determina la calidad y el tamaño
    #                (32K,64K,96k,128K,192K,256K,320K)
    # channels:      canales de audio (1:Mono, 2:Estéreo, 3: tres canales... hasta el 8)
    # sample_rate:   frecuencia de muestreo( 8kHz,22.05kHz,44.1kHz,48kHz,96kHz,192kHz)
    #                expresar con todos los ceros 8Khz=8000
    # volume:        volumen del audio puede aumentarse 1.5, o puede reducirse 0.5

