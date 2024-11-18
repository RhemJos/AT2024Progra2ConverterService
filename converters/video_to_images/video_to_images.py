#
# @video_to_images.py Copyright (c) 2021 Jalasoft.
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


class VideoToImagesConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, output_path=None, **kwargs):
        # Extract the fps value from kwargs, or use 1 as the default value
        fps = kwargs.get('fps', 1)

        # Convert video into a series of frames
        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', self.filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, '%d.jpg')

        # ffmpeg command to extract frames
        ffmpeg_command = ffmpeg.input(self.file_path)

        # Apply fps filter on input
        ffmpeg_command = ffmpeg_command.filter('fps', fps=fps)

        # Define command output
        ffmpeg_command = ffmpeg_command.output(output_path)

        try:
            # Run the ffmpeg command
            ffmpeg_command.run(overwrite_output=True)
            return frames_folder
        except ffmpeg.Error as e:
            # Capture and show the error if it occurs
            if e.stderr:
                print(f"Error executing ffmpeg command: {e.stderr}")
            else:
                print("Unknown error while running ffmpeg command.")
            raise
