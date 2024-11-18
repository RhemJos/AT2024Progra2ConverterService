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
from validators.int_validator import IntValidator
from validators.file_validator import FileValidator
from validators.validator_context import ValidatorContext
from exceptions.video_convert_exception import VideoConvertError

class VideoToImagesConverter(Converter):
    def __init__(self, video_path):
        super().__init__(video_path)

    def convert(self, **kwargs):
        fps = kwargs.get('fps', 1)
        output_path = kwargs.get('output_path')

        # Validate parameters
        self.validate_params(output_path=output_path, fps=fps)

        frames_folder = os.path.join('outputs', 'video_to_frames_outputs', self.filename)
        os.makedirs(frames_folder, exist_ok=True)

        if output_path is None:
            output_path = os.path.join(frames_folder, '%d.jpg')

        # Ffmpeg command to extract frames
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
            raise VideoConvertError(f"ffmpeg command execution failed: {e.stderr}", 500)


    def validate_params(self, **kwargs):
        validators = [ IntValidator(kwargs['fps'], True, "Fps"),
                       ]
        if kwargs['output_path']:
            validators.append(FileValidator(kwargs['output_path'], True, "Output directory") )

        validator_context = ValidatorContext(validators, VideoConvertError)
        validator_context.run_validations()
