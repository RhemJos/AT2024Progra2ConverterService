from validators.validator import Validator
from exceptions.video_convert_exception import VideoConvertError
from utils import get_args

OPTIONS = {
            "format": ["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
            "vcodec": ["libx264", "libx265", "mpeg4", "vp8", "vp9", "prores", "huffyuv", "hevc_nvenc"],
            "acodec": ["aac", "mp3", "opus", "ac3", "pcm_s16le", "vorbis"],
            "audio_channels": ['1', '2', '4', '6', '8']
        }

parameters = {
    "output_format" : None,  
    "vcodec" : None  ,
    "acodec" : None ,
     "r" : None ,
    "ac" : None 
}

class VideoValidator(Validator):
    def __init__(self):
        super().__init__(OPTIONS, VideoConvertError)
             
    def validate_video_format(self, output_format):
        self.validate_format(output_format, 'format',"Formato de salida")        

    def validate_vcodec(self, vcodec):
        self.validate_format(vcodec, 'vcodec',"Códec de video")       

    def validate_acodec(self, acodec): 
        self.validate_format(acodec, 'acodec',"Códec de audio")  

    def validate_fps(self, fps): # Opcional
        self.validate_int(fps, "Frames por segundo")

    def validate_audio_channels(self, audio_channels): # Opcional
        self.validate_int(audio_channels, "Canales de audio")
        self.validate_format(audio_channels, 'audio_channels',"Canales de audio")  

    def validate(self, **kwargs):
        params = get_args(parameters, kwargs)
        output_format = params["output_format"]
        vcodec =  params["vcodec"]
        acodec = params["acodec"]
        r = params["r"]
        ac =  params["ac"]
        if output_format:
            self.validate_video_format(output_format),
        if vcodec:
            self.validate_vcodec(vcodec),
        if acodec:
            self.validate_acodec(acodec),
        if r:
            self.validate_fps(r),
        if ac:
            self.validate_audio_channels(ac)
