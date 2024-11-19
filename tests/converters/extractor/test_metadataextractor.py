#
# @test_metadataextractor.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
from subprocess import CalledProcessError
import unittest
from unittest.mock import MagicMock, patch
from converters.extractor.metadataextractor import MetadataExtractor


class TestMetadataextractor(unittest.TestCase):

    # Positive test - give metadata extractor a valid image
    def test_metadataextractor(self):
        self.maxDiff = None
        meta_data_extractor = MetadataExtractor( r'.\tests\converters\extractor\image.jpeg')
        result = meta_data_extractor.extract()
        del result['File Access Date/Time           ']
        del result['File Modification Date/Time     ']
        del result['File Creation Date/Time         ']
        expected_result = {'ExifTool Version Number         ': ' 12.99',
        'File Name                       ': ' image.jpeg',
        'Directory                       ': ' ./tests/converters/extractor', 
        'File Size                       ': ' 141 kB', 
        'File Permissions                ': ' -rw-rw-rw-', 
        'File Type                       ': ' JPEG', 
        'File Type Extension             ': ' jpg', 
        'MIME Type                       ': ' image/jpeg', 
        'JFIF Version                    ': ' 1.01', 
        'Resolution Unit                 ': ' None',
        'X Resolution                    ': ' 1', 
        'Y Resolution                    ': ' 1', 
        'Image Width                     ': ' 996', 
        'Image Height                    ': ' 1356', 
        'Encoding Process                ': ' Progressive DCT, Huffman coding', 
        'Bits Per Sample                 ': ' 8', 
        'Color Components                ': ' 3', 
        'Y Cb Cr Sub Sampling            ': ' YCbCr4:2:0 (2 2)', 
        'Image Size                      ': ' 996x1356', 
        'Megapixels                      ': ' 1.4'}
        self.assertEqual(result,expected_result)
    
    # Postive test - give metadata extractor a valid image with a name containing spaces
    def test_metadataextractor_file_name_with_spaces(self):
        self.maxDiff = None
        meta_data_extractor = MetadataExtractor( r'.\tests\converters\extractor\image edited.png')
        result = meta_data_extractor.extract()
        print(str(result))
        del result['File Access Date/Time           ']
        del result['File Modification Date/Time     ']
        del result['File Creation Date/Time         ']
        expected_result =  {'ExifTool Version Number         ': ' 12.99', 
                            'File Name                       ': ' image edited.png', 
                            'Directory                       ': ' ./tests/converters/extractor', 
                            'File Size                       ': ' 1239 kB', 
                            'File Permissions                ': ' -rw-rw-rw-', 
                            'File Type                       ': ' PNG', 
                            'File Type Extension             ': ' png', 
                            'MIME Type                       ': ' image/png', 
                            'Image Width                     ': ' 996', 
                            'Image Height                    ': ' 1356', 
                            'Bit Depth                       ': ' 8', 
                            'Color Type                      ': ' RGB', 
                            'Compression                     ': ' Deflate/Inflate', 
                            'Filter                          ': ' Adaptive', 
                            'Interlace                       ': ' Noninterlaced', 
                            'Image Size                      ': ' 996x1356', 
                            'Megapixels                      ': ' 1.4'}
        self.assertEqual(result,expected_result)

    # Postive test - give metadata extractor a linux plataform system
    @patch("converters.extractor.metadataextractor.CommandExecutor")
    @patch("converters.extractor.metadataextractor.platform.system")
    def test_metadataextractor_linux(self, mock_platform_system, MockCommandExecutor):
        # Configurar mocks
        self.maxDiff = None
        mock_platform_system.return_value = "Linux"
        mock_cmd = MockCommandExecutor.return_value
        mock_cmd.run_command.return_value = "key: value\n"
        meta_data_extractor = MetadataExtractor( r'.\tests\converters\extractor\image.jpeg')
        result = meta_data_extractor.extract()
        expected_result = {'key': ' value'}
        self.assertEqual(result,expected_result)
    
    # Postive test - give metadata extractor a windows plataform system
    @patch("converters.extractor.metadataextractor.CommandExecutor")
    @patch("converters.extractor.metadataextractor.platform.system")
    def test_metadataextractor_windows(self, mock_platform_system, MockCommandExecutor):
        self.maxDiff = None
        mock_platform_system.return_value = "Windows"
        mock_cmd = MockCommandExecutor.return_value
        mock_cmd.run_command.return_value = "key: value\n"
        meta_data_extractor = MetadataExtractor( r'.\tests\converters\extractor\image.jpeg')
        result = meta_data_extractor.extract()
        expected_result = {'key': ' value'}
        self.assertEqual(result,expected_result)
        
    # Negative test - give metadata extractor a invalid file path
    def test_metadataextractor_with_invalid_file_path(self):
        self.maxDiff = None
        with self.assertRaises(CalledProcessError) as cpe:
            meta_data_extractor = MetadataExtractor( r'.\tests\converters\extractor\invalid image.jpeg')
            meta_data_extractor.extract()