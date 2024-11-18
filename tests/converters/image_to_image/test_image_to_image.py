#
# @test_image_to_image.py Copyright (c) 2021 Jalasoft.
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

from converters.image_to_image.image_converter import ImageConverter


class TestImageToImage(unittest.TestCase):

    # Positive test - send image without changes
    def test_converter_image_to_image(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        path_converted_image = converter.convert()
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(path_converted_image,path_output_video)
    
    # Positive test - send image with output format
    def test_converter_image_to_image_with_output_format(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        format='png'
        converted_output_path = converter.convert(output_format=format)
        path_output_video = r'outputs\image_converted_outputs\image_edited.png'
        self.assertEqual(converted_output_path,path_output_video)
    
    # Positive test - send image with all the posible fields
    def test_converter_image_to_image_with_kwargs(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", 
            "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE"]
        output_path = converter.convert(resize=(600,600), resize_type="THUMBNAIL", output_format="png", 
                                        angle=3605, grayscale=True, filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.png'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize type cover
    def test_converter_image_to_image_with_resize_type_cover(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize=(600,600), resize_type="COVER")
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize type fit
    def test_converter_image_to_image_with_resize_type_fit(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize=(600,600), resize_type="FIT")
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize type pad
    def test_converter_image_to_image_with_resize_type_pad(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize=(600,600), resize_type="PAD")
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with no width
    def test_converter_image_to_image_with_no_width_measurement(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize=[None,1000])
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)
    
    # Positive test - send image with no height
    def test_converter_image_to_image_with_no_height_measurement(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize=[1000,None])
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Negative test - send image with invalid file path 
    def test_convert_image_with_invalid_file_path(self):
        with self.assertRaises(ValueError) as ve:
            file_path = r'.\tests\converters\image_to_image\image_none.jpeg'
            converter = ImageConverter(file_path)
            converter.convert()
        self.assertIn("The file is not a valid image", ve.exception.args[0])
    
    # Negative test - send image with invalid angle rotation
    def test_converter_image_with_invalid_rotation(self):
        with self.assertRaises(Exception) as ve:
            file_path = r'.\tests\converters\image_to_image\image.jpeg'
            converter = ImageConverter(file_path)
            output_path = converter.convert(angle='noveinta grados')
    
    # Negative - Positive test - send image with invalid filter
    def test_converter_image_to_image_with_invalid_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["Mean Filter"]
        output_path = converter.convert(filters=filters)
    
    # Negative test - send image with only one measure
    def test_converter_image_to_image_with_one_measurement(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ValueError) as ve:
            converter.convert(resize=[600])
        self.assertIn("Resize must be of type (width, height)", ve.exception.args[0])
    
    # Negative test - send image with invalid measurment 
    def test_converter_image_to_image_with_invalid_measurement(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(TypeError) as te:
            converter.convert(resize=['cien','cien'])
        self.assertIn("'str' object cannot be interpreted as an integer", te.exception.args[0])


    #Negative test - send image with invalid resize type
    def test_converter_image_to_image_with_invalid_resize_type(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ValueError) as te:
            converter.convert(resize=[1000,1000],resize_type="INVALID")
        self.assertIn("The resize type entered is not recognized", te.exception.args[0])

    # Negative test - send image with invalid output format
    def test_converter_image_to_image_with_invalid_output_format(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ValueError) as ve:
            converter.convert(output_format="mp3")
        self.assertEqual("Image conversion format not supported.",ve.exception.args[0])
    

        