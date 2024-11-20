#
# @test_audio_routes.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import os
import unittest
from flask import Flask
from unittest.mock import patch
from pathlib import Path
from models import File
from routes.audio_routes import audio_blueprint


class TestAudioRoutes(unittest.TestCase):
    # Set up database and routes for audio converter
    audio_path = Path(__file__).parent

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(audio_blueprint)
        cls.client = cls.app.test_client()

    def setUp(self):
        self.output_path=""

    def tearDown(self):
        if self.output_path:
            os.remove("outputs/audio_converted_outputs/"+self.output_path)

    # Positive, with valid audio file and output_format and all parameters
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_success(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "bit_rate": "32K", "channels": "2", "sample_rate": "8000", "volume": "0.5",
                "language_channel": "0", "speed": "1.2", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        data = response.get_json()
        print(data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format no parameters
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_no_parameters(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        data = response.get_json()
        print(data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format and bit_rate
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_and_bit_rate(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "bit_rate": "32K", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format and channels
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_and_channels(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "channels": "2", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format and sample_rate
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_and_sample_rate(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "sample_rate": "8000", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format and volume
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_and_volume(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "volume": "0.5", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format and language_channel
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_and_language_channel(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "language_channel": "0", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Positive, with valid audio file and output_format and speed
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_and_format_and_speed(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "speed": "1.2", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.output_path=response.json['download_URL'].split("/")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"],"Audio converted successfully.")

    # Negative, with valid audio file no output_format
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_valid_audio_no_format(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],"Audio converter: Output format: 'None' is not a valid option. Supported options: ['mp3', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv'].")

    # Negative, with audio file which extension was changed
    # jpg --> wav, image does not contain audio and an exception is raised
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_invalid_audio_image_extension_changed(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "JPG.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "audio": (self.audio_path / "JPG.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"],"Audio converter: Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)")

    #  --FALSE NEGATIVE-- Negative, with audio file which extension was changed
    #  mp4 --> wav, video contains audio and gets recognized as audio, but it should not
    @unittest.skip("TODO - implement a file verifier to catch modified files(video->audio)")
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_invalid_audio_video_extension_changed(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "MP4.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "audio": (self.audio_path / "MP4.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"],"Audio converter: Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)")

    # Negative, with audio file which extension was changed - pdf file
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_invalid_audio_file_extension_changed_pdf(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "PDF.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "audio": (self.audio_path / "PDF.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"],"Audio converter: Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)")

    # Negative, with audio file corrupted
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_invalid_audio_corrupted(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "corrupt.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "audio": (self.audio_path / "corrupt.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"],
                         "Audio converter: Ffmpeg command for audio convertion failed: ffmpeg error (see stderr output for detail)")

    # Negative, with invalid output_format
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_output_format(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "invalid_output_format", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],
                         "Audio converter: Output format: 'invalid_output_format' is not a valid option. Supported options: ['mp3', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv'].")

    # Negative, with invalid bit_rate
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_bit_rate(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "bit_rate": "invalid_bit_rate", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],
                         "Audio converter: Bit rate: 'invalid_bit_rate' is not a valid option. Supported options: ['32K', '64K', '96K', '128K', '192K', '256K', '320K'].")

    # Negative, with invalid channels
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_channels(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "channels": "invalid_channels", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],
                         "Audio converter: Audio channels: 'invalid_channels' is not a valid option. Supported options: ['1', '2', '3', '4', '5', '6', '7', '8'].")

    # Negative, with invalid sample_rate
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_sample_rate(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "sample_rate": "invalid_sample_rate", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],
                         "Audio converter: Sample rate: 'invalid_sample_rate' is not a valid option. Supported options: ['8000', '22050', '44100', '48000', '96000', '192000'].")

    # Negative, with invalid volume
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_volume(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "volume": "invalid_volume", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],
                         "Audio converter: Volume: 'invalid_volume' is not a valid option. Supported options: ['0.5', '1.5'].")

    # Negative, with invalid language_channel
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_language_channel(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "language_channel": "invalid_language_channel", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],
                         "Audio converter: Language channel must be an integer.")

# NOTE - speed has two different error messages when the input is string and when it exceeds the [0.5,2.0] limit
    # Negative, with invalid speed string
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_speed(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "speed": "invalid_speed", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],"Audio converter: Speed must be a number")
        ################################

    # Negative, with invalid speed number
    @patch('routes.audio_routes.get_or_save')
    def test_audio_route_with_invalid_speed_number(self,mock_get_or_save):
        file = File(file_extension="wav",
                    checksum="audio",
                    file_path=os.path.join("tests", "routes", "audio.wav"),
                    output_path="")
        mock_get_or_save.return_value = (True, file)
        data = {"output_format": "ogg", "speed": "3", "audio": (self.audio_path / "audio.wav").open("rb")}
        response = self.client.post('/convert-audio', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"],"Audio converter: Speed must be a number between [0.5, 2.0]")
