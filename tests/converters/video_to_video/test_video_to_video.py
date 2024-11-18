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

import unittest
import ffmpeg
import os
from converters.video_to_video.video_to_video import VideoToVideoConverter


class TestVideoToVideoConverter(unittest.TestCase):

    # define output_path to remove it at the end of tests
    def setUp(self):
        self.output_path = ""

    def tearDown(self):
        # remove converted_videos
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    # Positive, with valid video_path and output_format and all kwargs
    def test_video_converter_success(self):
        video_path = os.path.join("tests","converters", "video_to_video","video.mp4")
        converter = VideoToVideoConverter(video_path)
        self.output_path = converter.convert(
            output_format="avi",
            fps=24,
            video_codec="libx265",
            audio_codec="mp3",
            audio_channels=2,
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid video_path and output_format no kwargs
    def test_video_converter_valid_video_path_and_format_no_kwargs(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        self.output_path = converter.convert(
            output_format="avi",
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid video_path and output_format and fps
    def test_video_converter_valid_video_path_and_format_and_fps(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        self.output_path = converter.convert(
            output_format="avi",
            fps=24,
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid video_path and output_format and video_codec
    def test_video_converter_valid_video_path_and_format_and_video_codec(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        self.output_path = converter.convert(
            output_format="avi",
            video_codec="libx265",
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid video_path and output_format and audio_codec
    def test_video_converter_valid_video_path_and_format_and_audio_codec(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        self.output_path = converter.convert(
            output_format="avi",
            audio_codec="mp3",
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid video_path and output_format and audio_channels
    def test_video_converter_valid_video_path_and_format_and_audio_channels(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        self.output_path = converter.convert(
            output_format="avi",
            audio_channels=2,
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Negative, with video_path as None
    def test_video_converter_invalid_input_None(self):
        video_path = None
        with self.assertRaises(TypeError):
            converter = VideoToVideoConverter(video_path)

    # Negative, with video_path as empty string
    def test_video_converter_invalid_input_empty(self):
        video_path = ""
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ffmpeg.Error):
            self.output_path = converter.convert(
                output_format="avi",
            )

    # Negative, with video_path that does not exist
    def test_video_converter_video_path_does_not_exist(self):
        video_path = os.path.join( "does_not_exist.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ffmpeg.Error):
            self.output_path = converter.convert(
                output_format="avi",
            )

    # --ERROR-- Negative, with video_path which extension was changed - audio files
    #  ogg --> mp4, the conversion worked and created a video with only audio, but it should not
    def test_video_converter_input_audio_file_extension_changed(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "OGG.mp4")
        with self.assertRaises(Exception):
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )

    # --ERROR-- Negative, with video_path which extension was changed - image files
    #  jpg --> mp4, the conversion worked and created a video with only an image, but it should not
    def test_video_converter_input_image_file_extension_changed(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "JPG.mp4")
        with self.assertRaises(Exception):
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )

    # Negative, with video_path which extension was changed - pdf file
    def test_video_converter_input_files_extension_changed_pdf(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "PDF.mp4")
        with self.assertRaises(ffmpeg.Error):
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )

    # Negative, with video_path which extension was changed - pdf file
    def test_video_converter_input_files_extension_changed_txt(self):
        video_path = os.path.join("tests", "converters", "video_to_video","text.mp4")
        with self.assertRaises(ffmpeg.Error):
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )

    # Negative, with video_path corrupted
    def test_video_converter_video_corrupted(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "corrupt.mp4")
        with self.assertRaises(ffmpeg.Error):
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )

    # Negative, without parameters
    def test_video_converter_without_parameters(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ffmpeg.Error):
            self.output_path = converter.convert()

    # Negative, with invalid format
    def test_video_converter_with_invalid_output_format(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ffmpeg.Error):
            self.output_path = converter.convert(
                output_format="invalid_format"
            )

    # Negative, with invalid fps
    def test_video_converter_with_invalid_fps(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ValueError):
            self.output_path = converter.convert(
                output_format="avi",
                fps="invalid_fps"
            )

    # Negative, with invalid video codec
    def test_video_converter_with_invalid_video_codec(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ffmpeg.Error):
            self.output_path = converter.convert(
                output_format="avi",
                video_codec="invalid_video_codec"
            )

    # Negative, with invalid audio codec
    def test_video_converter_with_invalid_audio_codec(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "vid.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ffmpeg.Error):
            self.output_path = converter.convert(
                output_format="avi",
                audio_codec="invalid_audio_codec"
            )

    # Negative, with invalid audio channels
    def test_video_converter_with_invalid_audio_channels(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(ValueError):
            self.output_path = converter.convert(
                output_format="avi",
                audio_channels="invalid_audio_channels"
            )
