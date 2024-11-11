

class VideoValidator:
    OPTIONS = {
        "format": ["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
        "vcodec": ["libx264", "libx265", "mpeg4", "vp8", "vp9", "prores", "huffyuv", "hevc_nvenc"],
        "acodec": ["aac", "mp3", "opus", "ac3", "pcm_s16le", "vorbis"],
        "audio_channels": [1, 2, 4, 6, 8]
    }

    @staticmethod
    def validate_format(output_format):
        if output_format not in VideoValidator.OPTIONS["format"]: # Obligatorio
            return f"Formato de salida '{output_format}' no es válido."
        return None

    @staticmethod
    def validate_vcodec(vcodec):
        if vcodec and vcodec not in VideoValidator.OPTIONS["vcodec"]: # Opcional
            return f"Códec de video '{vcodec}' no es válido."
        return None

    @staticmethod
    def validate_acodec(acodec): 
        if acodec and acodec not in VideoValidator.OPTIONS["acodec"]: # Opcional
            return f"Códec de audio '{acodec}' no es válido."
        return None

    @staticmethod
    def validate_fps(fps): # Opcional
        if fps:
            try:
                fps = int(fps)
            except ValueError:
                return "El número de frames por segundo debe ser un número entero."
        return None

    @staticmethod
    def validate_audio_channels(audio_channels): # Opcional
        if audio_channels:
            try:
                audio_channels = int(audio_channels)
            except ValueError:
                return "El número de canales de audio debe ser un número entero."
            if audio_channels not in VideoValidator.OPTIONS["audio_channels"]:
                return f"Canales de audio '{audio_channels}' no es válido. Opciones válidas: {VideoValidator.OPTIONS['audio_channels']}."
        return None

    @staticmethod
    def validate(output_format, vcodec, acodec, fps, audio_channels):
        errors = [
            VideoValidator.validate_format(output_format),
            VideoValidator.validate_vcodec(vcodec),
            VideoValidator.validate_acodec(acodec),
            VideoValidator.validate_fps(fps),
            VideoValidator.validate_audio_channels(audio_channels)
        ]

        return [error for error in errors if error] # List comprehension