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
from exceptions.audio_convert_exception import AudioConvertError



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
            output_format="mp3",
            bit_rate="32K",
            channels="2",
            sample_rate="8000",
            volume="1.5",
            language_channel=0,
            speed=1.2
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format no kwargs
    def test_audio_converter_valid_audio_path_and_format_no_kwargs(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and bit_rate
    def test_audio_converter_valid_audio_path_and_format_and_bit_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
            bit_rate="32K"
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and channels
    def test_audio_converter_valid_audio_path_and_format_and_channels(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
            channels="2"
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and sample_rate
    def test_audio_converter_valid_audio_path_and_format_and_sample_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
            sample_rate="8000"
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and volume
    def test_audio_converter_valid_audio_path_and_format_and_volume(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
            volume="1.5"
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and language_channel
    def test_audio_converter_valid_audio_path_and_format_and_language_channel(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
            language_channel=0
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)

    # Positive, with valid audio_path and output_format and speed
    def test_audio_converter_valid_audio_path_and_format_and_speed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        self.output_path = converter.convert(
            output_format="mp3",
            speed=1.2
        )
        expected = os.path.join("outputs", "audio_converted_outputs", "audio.mp3")
        self.assertEqual(self.output_path, expected)
#FALLA REVISAR
    # Negative, without parameters. output_format is required
    def test_audio_converter_without_parameters(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert()
        self.assertIn("Output format: 'None' is not a valid option. Supported options: ['mp3', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv'].", ex.exception.args[0])

    # Negative, with audio_path as None - self.filename = os.path.splitext(os.path.basename(file_path))[0] produce el error
    def test_audio_converter_invalid_audio_path_None(self):
        audio_path = None
        with self.assertRaises(TypeError) as ex:
            converter = AudioConverter(audio_path)
        self.assertIn("expected str, bytes or os.PathLike object, not NoneType", ex.exception.args[0])


    # Negative, with audio_path as empty string
    def test_audio_converter_invalid_audio_path_empty(self):
        audio_path = ""
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3"
            )
        self.assertIn("Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    # Negative, with audio_path that does not exist
    def test_audio_converter_audio_path_does_not_exist(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "does_not_exist.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3"
            )
        self.assertIn("Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    # Negative, with audio_path which extension was changed
    # jpg --> wav, image does not contain audio and an exception is raised
    def test_audio_converter_audio_path_image_extension_changed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "JPG.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3"
            )
        self.assertIn("Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    #  --ERROR-- Negative, with audio_path which extension was changed
    #  mp4 --> wav, video contains audio and gets recognized as audio, but it should not
    @unittest.skip("TODO - implement a file verifier to catch modified files(video->audio)")
    def test_audio_converter_audio_path_video_extension_changed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "MP4.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError):
            self.output_path = converter.convert(
                output_format="mp3"
            )

    # Negative, with audio_path which extension was changed - pdf file
    def test_audio_converter_audio_path_files_extension_changed_pdf(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "PDF.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3"
            )
        self.assertIn("Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    # Negative, with audio_path which extension was changed - txt file
    def test_audio_converter_audio_path_files_extension_changed_txt(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio","text.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3"
            )
        self.assertIn("Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    # Negative, with audio_path corrupted
    def test_audio_converter_audio_path_corrupted(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "corrupt.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3"
            )
        self.assertIn("Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)", ex.exception.args[0])


    # Negative, with invalid output_format
    def test_audio_converter_with_invalid_output_format(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="invalid_format"
            )
        self.assertIn("Output format: 'invalid_format' is not a valid option. Supported options: ['mp3', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv'].", ex.exception.args[0])

    # Negative, with invalid bit_rate
    def test_audio_converter_with_invalid_bit_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                bit_rate="invalid_bit_rate"
            )
        self.assertIn("Bit rate: 'invalid_bit_rate' is not a valid option. Supported options: ['32K', '64K', '96K', '128K', '192K', '256K', '320K'].", ex.exception.args[0])


    # Negative, with invalid channels
    def test_audio_converter_with_invalid_channels(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                channels="invalid_channels"
            )
        self.assertIn("Audio channels: 'invalid_channels' is not a valid option. Supported options: ['1', '2', '3', '4', '5', '6', '7', '8'].", ex.exception.args[0])


    # Negative, with invalid sample_rate
    def test_audio_converter_with_invalid_sample_rate(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                sample_rate="invalid_sample_rate"
            )
        self.assertIn("Sample rate: 'invalid_sample_rate' is not a valid option. Supported options: ['8000', '22050', '44100', '48000', '96000', '192000'].", ex.exception.args[0])

    # Negative, with invalid volume
    def test_audio_converter_with_invalid_volume(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                volume="invalid_volume"
            )
        self.assertIn("Volume: 'invalid_volume' is not a valid option. Supported options: ['0.5', '1.5'].", ex.exception.args[0])

    # Negative, with invalid language_channel
    def test_audio_converter_with_invalid_language_channel(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                language_channel="invalid_language_channel"
            )
        self.assertIn("Language channel must be an integer.", ex.exception.args[0])

    # Negative, with invalid speed string
    def test_audio_converter_with_invalid_speed(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                speed="invalid_speed"
            )
        self.assertIn("Speed must be a number", ex.exception.args[0])


    # Negative, with invalid speed number
    def test_audio_converter_with_invalid_speed_number(self):
        audio_path = os.path.join("tests", "converters", "audio_to_audio", "audio.wav")
        converter = AudioConverter(audio_path)
        with self.assertRaises(AudioConvertError) as ex:
            self.output_path = converter.convert(
                output_format="mp3",
                speed=5
            )
        self.assertIn("Speed must be a number between [0.5, 2.0]", ex.exception.args[0])


