from validators.validator import Validator


class FormatValidator(Validator):
    # options = {
    #         "format": ["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
    #         "vcodec": ["libx264", "libx265", "mpeg4", "vp8", "vp9", "prores", "huffyuv", "hevc_nvenc"],
    #         "acodec": ["aac", "mp3", "opus", "ac3", "pcm_s16le", "vorbis"],
    #         "audio_channels": ['1', '2', '4', '6', '8']
    #     }
    
    def __init__(self, entered_format, valid_options: list, param_name):
        super().__init__( param_name)
        self.entered_format = entered_format
        self.valid_options = valid_options

    def validate(self):
        print(self.entered_format, self.valid_options)
        if self.entered_format not in self.valid_options:  
            message = f"{self.param_name}: '{self.entered_format}' no es válido. Opciones válidas: {self.valid_options}."
            raise self.error_class( message, 400)