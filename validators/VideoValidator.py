#
# @VideoValidator.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

class VideoValidator:  # Define valid options for video format, video codec, audio codec, and audio channels
    OPTIONS = {
        "format": ["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"],
        "vcodec": ["libx264", "libx265", "mpeg4", "vp8", "vp9", "prores", "huffyuv", "hevc_nvenc"],
        "acodec": ["aac", "mp3", "opus", "ac3", "pcm_s16le", "vorbis"],
        "audio_channels": [1, 2, 4, 6, 8]
    }

    @staticmethod
    def validate_format(output_format):  # Validate if the output format is in the allowed list
        if output_format not in VideoValidator.OPTIONS["format"]:  # obligatory
            return f"Output format '{output_format}' is not valid."
        return None

    @staticmethod
    def validate_vcodec(vcodec):  # Validate if the video codec is in the allowed list (optional)
        if vcodec and vcodec not in VideoValidator.OPTIONS["vcodec"]:  # optional
            return f"Video codec '{vcodec}' is not valid."
        return None

    @staticmethod
    def validate_acodec(acodec):  # Validate if the audio codec is in the allowed list (optional)
        if acodec and acodec not in VideoValidator.OPTIONS["acodec"]:  # optional
            return f"Audio codec '{acodec}' is not valid."
        return None

    @staticmethod
    def validate_fps(fps):  # Validate if frames per second is a valid integer (optional)
        if fps:
            try:
                fps = int(fps)
            except ValueError:
                return "The number of frames per second must be an integer."
        return None

    @staticmethod  # Validate if the number of audio channels is an integer and in the allowed list
    def validate_audio_channels(audio_channels):  # optional
        if audio_channels:
            try:
                audio_channels = int(audio_channels)
            except ValueError:
                return "The number of audio channels must be an integer."
            if audio_channels not in VideoValidator.OPTIONS["audio_channels"]:
                return f"Audio channels '{audio_channels}' is not valid. Valid options: {VideoValidator.OPTIONS['audio_channels']}."
        return None

    @staticmethod  # Validate all parameters and collect errors in a list
    def validate(output_format, vcodec, acodec, fps, audio_channels):
        errors = [
            VideoValidator.validate_format(output_format),
            VideoValidator.validate_vcodec(vcodec),
            VideoValidator.validate_acodec(acodec),
            VideoValidator.validate_fps(fps),
            VideoValidator.validate_audio_channels(audio_channels)
        ]

        return [error for error in errors if error]  # List comprehension
