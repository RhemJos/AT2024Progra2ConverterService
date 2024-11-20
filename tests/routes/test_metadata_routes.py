#
# @test_metadata_routes.py Copyright (c) 2021 Jalasoft.
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
from unittest.mock import patch
from flask import Flask
from werkzeug.datastructures import FileStorage
from routes.metadata_routes import metadata_blueprint


class TestMetadataRoutes(unittest.TestCase):
    def setUp(self):
        # Create Flask instance and register blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(metadata_blueprint)
        self.client = self.app.test_client()  # Test client

    # Positive test - send a valid video
    @patch('os.remove')    
    @patch('routes.metadata_routes.save_file')
    def test_get_metadata_of_a_video(self, mock_save_file, mock_os_remove):
        self.maxDiff = None
        temp_file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.return_value =r'.\tests\routes\2024-11-12 10-27-31.mkv'
        
        with open(temp_file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/get-metadata', data=data, content_type='multipart/form-data')
        mock_os_remove.assert_called_once_with(r'.\tests\routes\2024-11-12 10-27-31.mkv')   
        self.assertEqual(response.status_code, 200)
        result = response.json
        del result['File Access Date/Time           ']
        del result['File Modification Date/Time     ']
        del result['File Creation Date/Time         ']
        expected_result={'Audio Bits Per Sample           ': ' 16', 
                         'Audio Channels                  ': ' 2', 
                         'Audio Sample Rate               ': ' 48000', 
                         'Codec ID                        ': ' A_AAC', 
                         'Directory                       ': ' ./tests/routes', 
                         'Display Unit                    ': ' Unknown', 
                         'Doc Type                        ': ' matroska', 
                         'Doc Type Read Version           ': ' 2', 
                         'Doc Type Version                ': ' 4', 
                         'Duration                        ': ' 00:00:03.264000000', 
                         'EBML Read Version               ': ' 1', 
                         'EBML Version                    ': ' 1', 
                         'Encoder                         ': ' Lavf58.29.100', 
                         'ExifTool Version Number         ': ' 12.99', 
                         'File Name                       ': ' 2024-11-12 10-27-31.mkv', 
                         'File Permissions                ': ' -rw-rw-rw-', 
                         'File Size                       ': ' 1145 kB', 
                         'File Type                       ': ' MKV', 
                         'File Type Extension             ': ' mkv', 
                         'Image Height                    ': ' 1080', 
                         'Image Size                      ': ' 1920x1080', 
                         'Image Width                     ': ' 1920', 
                         'MIME Type                       ': ' video/x-matroska', 
                         'Megapixels                      ': ' 2.1', 
                         'Muxing App                      ': ' Lavf58.29.100', 
                         'Tag Track UID                   ': ' 02', 
                         'Timecode Scale                  ': ' 1 ms', 
                         'Track Language                  ': ' und', 
                         'Track Name                      ': ' simple_aac', 
                         'Track Number                    ': ' 2', 
                         'Track Type                      ': ' Audio', 
                         'Track UID                       ': ' 02', 
                         'Video Frame Rate                ': ' 30', 
                         'Writing App                     ': ' Lavf58.29.100'}
        self.assertEqual(result,expected_result)

    # Positive test - send a valid image
    @patch('os.remove')    
    @patch('routes.metadata_routes.save_file')
    def test_get_metadata_of_a_image(self, mock_save_file, mock_os_remove):
        self.maxDiff = None
        temp_file = r'.\tests\routes\image.jpeg'
        mock_save_file.return_value =r'.\tests\routes\image.jpeg'
        
        with open(temp_file, 'rb') as f:
            data = {
                'file': (FileStorage(f), 'image.jpeg')
            }
            response = self.client.post('/get-metadata', data=data, content_type='multipart/form-data')
        mock_os_remove.assert_called_once_with(r'.\tests\routes\image.jpeg')   
        self.assertEqual(response.status_code, 200)
        result = response.json
        del result['File Access Date/Time           ']
        del result['File Modification Date/Time     ']
        del result['File Creation Date/Time         ']
        expected_result={'Bits Per Sample                 ': ' 8', 
                         'Color Components                ': ' 3', 
                         'Directory                       ': ' ./tests/routes', 
                         'Encoding Process                ': ' Progressive DCT, Huffman coding', 
                         'ExifTool Version Number         ': ' 12.99', 
                         'File Name                       ': ' image.jpeg', 
                         'File Permissions                ': ' -rw-rw-rw-', 
                         'File Size                       ': ' 141 kB', 
                         'File Type                       ': ' JPEG', 
                         'File Type Extension             ': ' jpg', 
                         'Image Height                    ': ' 1356', 
                         'Image Size                      ': ' 996x1356', 
                         'Image Width                     ': ' 996', 
                         'JFIF Version                    ': ' 1.01', 
                         'MIME Type                       ': ' image/jpeg', 
                         'Megapixels                      ': ' 1.4', 
                         'Resolution Unit                 ': ' None', 
                         'X Resolution                    ': ' 1', 
                         'Y Cb Cr Sub Sampling            ': ' YCbCr4:2:0 (2 2)',
                         'Y Resolution                    ': ' 1'}
        self.assertEqual(result,expected_result)
    
    # Positive test - send a valid file with a name containing spaces
    @patch('os.remove')    
    @patch('routes.metadata_routes.save_file')
    def test_get_metadata_of_a_image_with_spaces(self, mock_save_file, mock_os_remove):
        self.maxDiff = None
        temp_file = r'.\tests\routes\image edited.png'
        mock_save_file.return_value =r'.\tests\routes\image edited.png'
        
        with open(temp_file, 'rb') as f:
            data = {
                'file': (FileStorage(f), 'image edited.png')
            }
            response = self.client.post('/get-metadata', data=data, content_type='multipart/form-data')
        mock_os_remove.assert_called_once_with(r'.\tests\routes\image edited.png')   
        self.assertEqual(response.status_code, 200)
        result = response.json
        del result['File Access Date/Time           ']
        del result['File Modification Date/Time     ']
        del result['File Creation Date/Time         ']
        expected_result={'Bit Depth                       ': ' 8',
                        'Color Type                      ': ' RGB',
                        'Compression                     ': ' Deflate/Inflate', 
                        'Directory                       ': ' ./tests/routes', 
                        'ExifTool Version Number         ': ' 12.99', 
                        'File Name                       ': ' image edited.png', 
                        'File Permissions                ': ' -rw-rw-rw-', 
                        'File Size                       ': ' 1239 kB', 
                        'File Type                       ': ' PNG', 
                        'File Type Extension             ': ' png', 
                        'Filter                          ': ' Adaptive', 
                        'Image Height                    ': ' 1356', 
                        'Image Size                      ': ' 996x1356', 
                        'Image Width                     ': ' 996', 
                        'Interlace                       ': ' Noninterlaced', 
                        'MIME Type                       ': ' image/png', 
                        'Megapixels                      ': ' 1.4'}
        self.assertEqual(result,expected_result)

    # Negative test - send a ValueError when using the method save_file
    @patch('os.remove')    
    @patch('routes.metadata_routes.save_file')
    def test_get_metadata_of_video_with_error(self, mock_save_file, mock_os_remove):
        self.maxDiff = None
        temp_file = r'.\tests\routes\2024-11-12 10-27-31.mkv'
        mock_save_file.side_effect = ValueError("No file in the request")
        
        with open(temp_file, 'rb') as f:
            data = {
                'file': (FileStorage(f), '2024-11-12 10-27-31.mkv')
            }
            response = self.client.post('/get-metadata', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "No file in the request"})
        