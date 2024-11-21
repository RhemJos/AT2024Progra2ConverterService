#
# @test_video_to_video.py Copyright (c) 2021 Jalasoft.
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
import os
from converters.video_to_video.video_to_video import VideoToVideoConverter
from exceptions.video_convert_exception import VideoConvertError


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
            audio_channels="2",
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
            audio_channels="2",
        )
        expected = os.path.join("outputs", "video_converted_outputs", "video-converted.avi")
        self.assertEqual(self.output_path, expected)

    # Negative, with video_path as None - self.filename = os.path.splitext(os.path.basename(file_path))[0]
    def test_video_converter_invalid_input_None(self):
        video_path = None
        with self.assertRaises(TypeError) as ex:
            converter = VideoToVideoConverter(video_path)
        self.assertIn("expected str, bytes or os.PathLike object, not NoneType", ex.exception.args[0])


    # Negative, with video_path as empty string
    def test_video_converter_invalid_input_empty(self):
        video_path = ""
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="avi",
            )
        self.assertIn("Ffmpeg command execution failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])

    # Negative, with video_path that does not exist
    def test_video_converter_video_path_does_not_exist(self):
        video_path = os.path.join( "does_not_exist.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="avi",
            )
        self.assertIn("Ffmpeg command execution failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    # --ERROR-- Negative, with video_path which extension was changed - audio files
    #  ogg --> mp4, the conversion worked and created a video with only audio, but it should not
    @unittest.skip("TODO - implement a file verifier to catch modified files(audio->video)")
    def test_video_converter_input_audio_file_extension_changed(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "OGG.mp4")
        with self.assertRaises(Exception):
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )

    # --ERROR-- Negative, with video_path which extension was changed - image files
    #  jpg --> mp4, the conversion worked and created a video with only an image, but it should not
    @unittest.skip("TODO - implement a file verifier to catch modified files(image->video)")
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
        with self.assertRaises(VideoConvertError) as ex:
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )
        self.assertIn("Ffmpeg command execution failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])

    # Negative, with video_path which extension was changed - txt file
    def test_video_converter_input_files_extension_changed_txt(self):
        video_path = os.path.join("tests", "converters", "video_to_video","text.mp4")
        with self.assertRaises(VideoConvertError) as ex:
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )
        self.assertIn("Ffmpeg command execution failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])

    # Negative, with video_path corrupted
    def test_video_converter_video_corrupted(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "corrupt.mp4")
        with self.assertRaises(VideoConvertError) as ex:
            converter = VideoToVideoConverter(video_path)
            self.output_path = converter.convert(
                output_format="avi",
            )
        self.assertIn("Ffmpeg command execution failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])

    # Negative, without parameters
    def test_video_converter_without_parameters(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert()
        self.assertIn("Output format: 'None' is not a valid option. Supported options: ['mp4', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv'].", ex.exception.args[0])

    # Negative, with invalid format
    def test_video_converter_with_invalid_output_format(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="invalid_format"
            )
        self.assertIn("Output format: 'invalid_format' is not a valid option. Supported options: ['mp4', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv'].", ex.exception.args[0])

    # Negative, with invalid fps
    def test_video_converter_with_invalid_fps(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="avi",
                fps="invalid_fps"
            )
        self.assertIn("Frames per second must be an integer.", ex.exception.args[0])


    # Negative, with invalid video codec
    def test_video_converter_with_invalid_video_codec(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="avi",
                video_codec="invalid_video_codec"
            )
        self.assertIn("Video codec: 'invalid_video_codec' is not a valid option. Supported options: ['libx264', 'libx265', 'mpeg4', 'vp8', 'vp9', 'prores', 'huffyuv', 'hevc_nvenc'].", ex.exception.args[0])

    # Negative, with invalid audio codec
    def test_video_converter_with_invalid_audio_codec(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "vid.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="avi",
                audio_codec="invalid_audio_codec"
            )
        self.assertIn("Audio codec: 'invalid_audio_codec' is not a valid option. Supported options: ['aac', 'mp3', 'opus', 'ac3', 'pcm_s16le', 'vorbis'].", ex.exception.args[0])


    # Negative, with invalid audio channels
    def test_video_converter_with_invalid_audio_channels(self):
        video_path = os.path.join("tests", "converters", "video_to_video", "video.mp4")
        converter = VideoToVideoConverter(video_path)
        with self.assertRaises(VideoConvertError) as ex:
            self.output_path = converter.convert(
                output_format="avi",
                audio_channels="invalid_audio_channels"
            )
        self.assertIn("Audio channels: 'invalid_audio_channels' is not a valid option. Supported options: ['1', '2', '4', '6', '8'].", ex.exception.args[0])
