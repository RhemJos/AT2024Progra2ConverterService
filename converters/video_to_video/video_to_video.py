#
# @video_to_video.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import ffmpeg
import os
from converters.converter import Converter


class VideoToVideoConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, output_format=None, **kwargs):
        temp_output_path = os.path.join('outputs', 'video_converted_outputs', f"{self.filename}-converted.{output_format}")
        output_path = os.path.join('outputs', 'video_converted_outputs', f"{self.filename}.{output_format}")
        # Initialize ffmpeg command with input
        ffmpeg_command = ffmpeg.input(self.file_path)
        # Add optional parameters to the output
        output_args = {}
        if 'fps' in kwargs and kwargs['fps']:
            output_args['r'] = int(kwargs['fps'])
        if 'video_codec' in kwargs and kwargs['video_codec']:
            output_args['vcodec'] = kwargs['video_codec']
        if 'audio_codec' in kwargs and kwargs['audio_codec']:
            output_args['acodec'] = kwargs['audio_codec']
        if 'audio_channels' in kwargs and kwargs['audio_channels']:
            output_args['ac'] = int(kwargs['audio_channels'])
        # Building the ffmpeg command with optional parameters in a single output
        ffmpeg_command = ffmpeg_command.output(temp_output_path, **output_args)
        try:  # Running the ffmpeg command
            ffmpeg_command.run(overwrite_output=True)
            return output_path
        except ffmpeg.Error as e:
            print(f"Error executing ffmpeg command: {e}")
            raise
