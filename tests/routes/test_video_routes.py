#
# @test_video_routes.py Copyright (c) 2021 Jalasoft.
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
from unittest.mock import MagicMock, patch
from flask import Flask
from werkzeug.datastructures import FileStorage
from exceptions.video_convert_exception import VideoConvertError
from routes.video_routes import video_blueprint


class TestVideoRoutes(unittest.TestCase):
    def setUp(self):
        # Create Flask instance and register blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(video_blueprint)
        self.client = self.app.test_client()  # Test client
    
    # VIDEO TO IMAGES UNIT TEST

    # Positive test - send a valid video 
    @patch('routes.video_routes.save_file')
    @patch('routes.video_routes.get_or_save')
    @patch('routes.video_routes.update')
    def test_video_routes_video_to_images(self,mock_update, mock_get_or_save, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file=MagicMock()
        mock_file.file_path =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.output_path = None
        mock_get_or_save.return_value = (False, mock_file)
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-images', data=data, content_type='multipart/form-data')
        mock_update.assert_called_once_with(mock_file)
        self.assertEqual(response.status_code, 200)
        result=response.json
        expected_result={'download_URL': 'http://localhost//api/download-frames/2024-11-12 10-27-31.zip', 
                         'message': 'Video processed successfully.', 
                         'output_path': '/outputs/video_to_frames_outputs/2024-11-12 10-27-31'}
        self.assertEqual(result,expected_result)

    # Positive test - send a video that already exist 
    @patch('routes.video_routes.save_file')
    @patch('routes.video_routes.get_or_save')
    def test_video_routes_video_to_images_video_already_exist(self, mock_get_or_save, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file=MagicMock()
        mock_file.file_path =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.output_path = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.checksum = "abc123"
        mock_get_or_save.return_value = (True, mock_file)
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-images', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        expected_result={'download_URL': 'http://localhost//api/download-frames/abc123.zip', 
                         'message': 'Video already exists in Database.', 
                         'output_path': '/.\\tests\\routes\\2024-11-12 10-27-31.mkv'}
        self.assertEqual(response.json,expected_result)

    # Negative test - error saving file - no video has been submited
    @patch('routes.video_routes.save_file')
    def test_video_routes_video_to_images_error_saving_file(self, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        file_type='video'
        mock_save_file.side_effect = ValueError(f"No {file_type} has been submitted in the request.")
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-images', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "No video has been submitted in the request."})
        
    # Negative test - error generating the checksum
    @patch('routes.video_routes.save_file')
    @patch('routes.video_routes.get_or_save')
    @patch('routes.video_routes.update')
    def test_video_routes_video_to_images_error_get_or_save(self,mock_update, mock_get_or_save, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file=MagicMock()
        file_path =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.output_path = None
        mock_get_or_save.side_effect = IOError(f"An error occured while generating file checksum of {file_path}")
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-images', data=data, content_type='multipart/form-data')
        self.assertEqual(response.json, {"error": 'Failed to save file to DB: An error occured while generating file checksum of .\\tests\\routes\\2024-11-12 10-27-31.mkv'})

    # Negative test - error in convert method 
    @patch('routes.video_routes.save_file')
    @patch('routes.video_routes.get_or_save')
    @patch('routes.video_routes.VideoToImagesConverter')
    def test_video_routes_video_to_images_error_convert(self,mock_class_converter, mock_get_or_save, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file=MagicMock()
        mock_file.file_path =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.output_path = None
        mock_get_or_save.return_value = (False, mock_file)
        mock_converter = MagicMock()
        mock_converter.convert.side_effect = VideoConvertError("Conversion failed", 500)
        mock_class_converter.return_value = mock_converter
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-images', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{'error': 'Video converter: Conversion failed'})

    # VIDEO TO VIDEO UNIT TEST

    # Positive test - send a valid video 
    @patch('routes.video_routes.save_file')
    @patch('routes.video_routes.get_or_save')
    def test_video_routes_video_to_video(self, mock_get_or_save, mock_save_file):#,mock_update
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file=MagicMock()
        mock_file.file_path =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.output_path = None
        mock_get_or_save.return_value = (False, mock_file)
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv'),
                'format':'mov'
            }
            response = self.client.post('/video-to-video', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        expected_result={'download_URL': 'http://localhost/api/download-video/2024-11-12 10-27-31-converted.mov',
                         'message': 'Video processed successfully.', 
                         'output_path': '/outputs/video_converted_outputs/2024-11-12 10-27-31.mov'}
        self.assertEqual(response.json,expected_result)

    # Negative test - error save file
    def test_video_routes_video_to_video_error_saving_file(self):
        file = r'.\tests\routes\image.jpeg'
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), 'image.jpeg')
            }
            response = self.client.post('/video-to-video', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,{'error': 'file format not supported.'})

    # Negative test - error saving in DB
    @patch('routes.video_routes.save_file')
    def test_video_routes_video_to_video_error_sending_DB(self, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-video', data=data, content_type='multipart/form-data')
        expected_result={'error': "Failed to save file to DB: The current Flask app is not registered with this 'SQLAlchemy' instance. Did you forget to call 'init_app', or did you create multiple 'SQLAlchemy' instances?"}
        self.assertEqual(response.json,expected_result)

    # Negative test - error in convert method 
    @patch('routes.video_routes.save_file')
    @patch('routes.video_routes.get_or_save')
    def test_video_routes_video_to_video_error_convert(self, mock_get_or_save, mock_save_file):
        file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file=MagicMock()
        mock_file.file_path =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_file.output_path = None
        mock_get_or_save.return_value = (False, mock_file)
        with open(file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/video-to-video', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        expected_result={'error': "Video converter: Output format: 'None' is not a valid option. Supported options: ['mp4', 'mov', 'avi', 'mkv', 'flv', 'webm', 'ogg', 'wmv']."}
        self.assertEqual(response.json,expected_result)