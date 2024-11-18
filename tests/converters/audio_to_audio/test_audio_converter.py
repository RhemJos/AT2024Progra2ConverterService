#
# @test_audio_converter.py Copyright (c) 2021 Jalasoft.
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
from converters.audio_to_audio.audio_converter import AudioConverter
from converters.audio_to_audio.audio_exception import AudioConversionError


class TestAudioConverter(unittest.TestCase):

    # define output_path to remove it at the end of tests
    def setUp(self):
        self.output_path = ""

    # remove converted_audios
    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    # Positive, with valid audio_path and output_format and all kwargs
    def test_audio_converter_success(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            bit_rate="32k",
            channels=2,
            sample_rate=8000,
            volume=1.5,
            language_channel=0,
            speed=1.2
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format no kwargs
    def test_audio_converter_valid_audio_path_and_format_no_kwargs(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and bit_rate
    def test_audio_converter_valid_audio_path_and_format_and_bit_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            bit_rate="32k"
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and channels
    def test_audio_converter_valid_audio_path_and_format_and_channels(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            channels=2
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and sample_rate
    def test_audio_converter_valid_audio_path_and_format_and_sample_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            sample_rate=8000
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and volume
    def test_audio_converter_valid_audio_path_and_format_and_volume(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            volume=1.5
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and language_channel
    def test_audio_converter_valid_audio_path_and_format_and_language_channel(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            language_channel=0
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and speed
    def test_audio_converter_valid_audio_path_and_format_and_speed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="m4a",
            speed=1.2
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.m4a")
        self.assertEqual(self.output_path, expected)

    # Positive, without parameters. The default format is mp3
    def test_audio_converter_without_parameters(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert()
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Negative, with audio_path as None
    def test_audio_converter_invalid_audio_path_None(self):
        audio_path = None
        with self.assertRaises(TypeError):
            converter = AudioConverter(audio_path)

    # Negative, with audio_path as empty string
    def test_audio_converter_invalid_audio_path_empty(self):
        audio_path = ""
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    # Negative, with audio_path that does not exist
    def test_audio_converter_audio_path_does_not_exist(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "does_not_exist.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    # Negative, with audio_path which extension was changed
    # jpg --> wav, image does not contain audio and an exception is raised
    def test_audio_converter_audio_path_image_extension_changed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "JPG.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    #  --ERROR-- Negative, with audio_path which extension was changed
    #  mp4 --> wav, video contains audio and gets recognized as audio, but it should not
    def test_audio_converter_audio_path_video_extension_changed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "MP4.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    # Negative, with audio_path which extension was changed - pdf file
    def test_audio_converter_audio_path_files_extension_changed_pdf(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "PDF.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    # Negative, with audio_path which extension was changed - txt file
    def test_audio_converter_audio_path_files_extension_changed_txt(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "outputs","audio_converted_outputs","text.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    # Negative, with audio_path corrupted
    def test_audio_converter_audio_path_corrupted(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "corrupt.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="m4a"
            )

    # Negative, with invalid output_format
    def test_audio_converter_with_invalid_output_format(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                output_format="invalid_format"
            )

    # Negative, with invalid bit_rate
    def test_audio_converter_with_invalid_bit_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                bit_rate="invalid_bit_rate"
            )

    # Negative, with invalid channels
    def test_audio_converter_with_invalid_channels(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                channels="invalid_channels"
            )

    # Negative, with invalid sample_rate
    def test_audio_converter_with_invalid_sample_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                sample_rate="invalid_sample_rate"
            )

    # Negative, with invalid volume
    def test_audio_converter_with_invalid_volume(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                volume="invalid_volume"
            )

    # Negative, with invalid language_channel
    def test_audio_converter_with_invalid_language_channel(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                language_channel="invalid_language_channel"
            )

    # --ERROR-- ValueError instead of AudioConversionError because is not a number and float() fails
    # Negative, with invalid speed
    def test_audio_converter_with_invalid_speed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                speed="invalid_speed"
            )

    # Negative, with invalid speed number
    def test_audio_converter_with_invalid_speed_number(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConversionError):
            self.output_path = converter.convert(
                speed=5
            )
