
class AudioOptions():
    def __init__(self):
        pass

    # construye el diccionario de opciones
    def build_options_audio(self, **kwargs) -> dict:
        options = {'vn': None}
        if 'bit_rate' in kwargs:
            options['b:a'] = kwargs['bit_rate']
        if 'channels' in kwargs:
            options['ac'] = kwargs['channels']
        if 'sample_rate' in kwargs:
            options['ar'] = kwargs['sample_rate']
        if 'volume' in kwargs:
            options['af'] = f"volume={kwargs['volume']}"
        if 'language_channel' in kwargs:
            options['map'] = f"0:a:{kwargs['language_channel']}"
        if 'speed' in kwargs:
            speed = float(kwargs['speed'])
            if 0.5 <= speed <= 2.0:
                if 'af' in options:
                    options['af'] += f",atempo={speed}"
                else:
                    options['af'] = f"atempo={speed}"
            else:
                print("La velocidad debe estar entre 0.5x y 2.0x")
                return None
        return options