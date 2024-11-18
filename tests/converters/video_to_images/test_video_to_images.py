#
# @test_video_to_images.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confide, ntial and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
import unittest
from unittest.mock import MagicMock, patch
import ffmpeg
from converters.video_to_images.video_to_images import VideoToImagesConverter


class Test_VideoToImages(unittest.TestCase):

    # Valid test - give converter a valid mkv video path and no output path
    def test_convert_video_mkv_to_images(self):
        video_path = r'.\tests\converters\video_to_images\2024-11-12 10-27-31.mkv'
        converter = VideoToImagesConverter(video_path)
        path_converted_video = converter.convert()
        path_output_video = r'outputs\video_to_frames_outputs\2024-11-12 10-27-31'
        self.assertEqual(path_converted_video,path_output_video)
    
    # Valid test - give converter a valid mp4 video path and no output path
    def test_convert_video_mp4_to_images(self):
        video_path = r'.\tests\converters\video_to_images\video_format_mp4.mp4'
        converter = VideoToImagesConverter(video_path)
        path_converted_video = converter.convert()
        path_output_video = r'outputs\video_to_frames_outputs\video_format_mp4'
        self.assertEqual(path_converted_video,path_output_video)

    # Positive test - give converter valid video path and output path
    def test_convert_video_to_images_with_output(self):
        video_path = r'.\tests\converters\video_to_images\2024-11-12 10-27-31.mkv'
        converter = VideoToImagesConverter(video_path)
        path_converted_video = converter.convert(r'tests\outputs\video_to_frames_outputs\2024-11-12 10-27-31\%d.jpg')
        path_output_video = r'outputs\video_to_frames_outputs\2024-11-12 10-27-31'
        self.assertEqual(path_converted_video,path_output_video)

    # Positive test - give converter valid video path, output path and fps
    def test_convert_video_to_images_with_kwargs(self):
        video_path = r'.\tests\converters\video_to_images\2024-11-12 10-27-31.mkv'
        converter = VideoToImagesConverter(video_path)
        path_converted_video = converter.convert(r'tests\outputs\video_to_frames_outputs\2024-11-12 10-27-31\%d.jpg', fps=10)
        path_output_video = r'outputs\video_to_frames_outputs\2024-11-12 10-27-31'
        self.assertEqual(path_converted_video,path_output_video)

    # Negative test - give converter a non-existence video path 
    def test_convert_video_to_images_invalid_path(self):
        with self.assertRaises(Exception): #Change the exception to video exception
            video_path = r'.\converters\video_to_images\2024-11-12 10-27-31.mkv'
            converter = VideoToImagesConverter(video_path)
            converter.convert()

    # Negative test - give converter valid video path and invalid output path - Error desconocido
    def test_convert_video_to_images_with_invalid_output(self):
        with self.assertRaises(ffmpeg.Error):
            video_path = r'.\tests\converters\video_to_images\2024-11-12 10-27-31.mkv'
            converter = VideoToImagesConverter(video_path)
            converter.convert(r'tests\outputs\video_to_frames_outputs\2024-11-12 10-27-31')
    
    # Negative test - give converter a mock that raisse an ffmpeg.Error when run is executed
    @patch('converters.video_to_images.video_to_images.ffmpeg.input')
    def test_ffmpeg_error_in_run(self, mock_ffmpeg_input):
        mock_command = MagicMock()
        mock_command.run.side_effect = ffmpeg.Error("Mock error", stderr=b"Formato de archivo no soportado", stdout=b"")

        # Configure methods for mock (input -> filter -> output -> run)
        mock_ffmpeg_input.return_value.filter.return_value.output.return_value = mock_command

        converter = VideoToImagesConverter('path/to/invalid_file.txt')
        
        with self.assertRaises(ffmpeg.Error) as cm:
            converter.convert()
        self.assertIn("Formato de archivo no soportado", cm.exception.stderr.decode('utf8'))

