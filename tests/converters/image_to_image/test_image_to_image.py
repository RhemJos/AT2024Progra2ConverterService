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
from exceptions.image_convert_exception import ImageConvertError


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
            "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE", "GRAYSCALE"]
        output_path = converter.convert(resize_width=600, resize_height = 600, resize_type="THUMBNAIL", output_format="png", 
                                        angle=360, filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.png'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with blur filter
    def test_converter_image_to_image_with_blur_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["BLUR"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with contour filter
    def test_converter_image_to_image_with_contour_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["CONTOUR"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with detail filter
    def test_converter_image_to_image_with_detail_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["DETAIL"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with edge enhance filter
    def test_converter_image_to_image_with_edge_enhance_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["EDGE_ENHANCE"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with edge enhance more filter
    def test_converter_image_to_image_with_edge_enhance__more_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["EDGE_ENHANCE_MORE"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with emboss filter
    def test_converter_image_to_image_with_emboss_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["EMBOSS"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with find edges filter
    def test_converter_image_to_image_with_find_edges_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["FIND_EDGES"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with sharpen filter
    def test_converter_image_to_image_with_sharpen_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["SHARPEN"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with smooth filter
    def test_converter_image_to_image_with_smooth_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["SMOOTH"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with smooth more filter
    def test_converter_image_to_image_with_smooth_more_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["SMOOTH_MORE"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with grayscale filter
    def test_converter_image_to_image_with_grayscale_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        filters=["GRAYSCALE"]
        output_path = converter.convert(filters=filters)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with a 0 angle
    def test_converter_image_to_image_with_angle_0(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(angle=0)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with a 360 angle
    def test_converter_image_to_image_with_angle_360(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(angle=360)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize type cover
    def test_converter_image_to_image_with_resize_type_cover(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize_width=600, resize_height = 600, resize_type="COVER")
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize type fit
    def test_converter_image_to_image_with_resize_type_fit(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize_width=600, resize_height = 600, resize_type="FIT")
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize type pad
    def test_converter_image_to_image_with_resize_type_pad(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize_width=600, resize_height = 600, resize_type="PAD")
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Positive test - send image with resize width (decimals)
    def test_converter_image_to_image_with_width_decimals(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path= converter.convert(resize_width=100.10,resize_height=1000)
        self.assertEqual(output_path,'outputs\\image_converted_outputs\\image_edited.jpeg')

    # Positive test - send image with resize height (decimals)
    def test_converter_image_to_image_with_height_decimals(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path= converter.convert(resize_height=100.10)
        self.assertEqual(output_path,'outputs\\image_converted_outputs\\image_edited.jpeg')

    # Positive test - send image with no width
    def test_converter_image_to_image_with_no_width_measurement(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize_height=1000)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)
    
    # Positive test - send image with no height
    def test_converter_image_to_image_with_no_height_measurement(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        output_path = converter.convert(resize_width=1000)
        path_output_video = r'outputs\image_converted_outputs\image_edited.jpeg'
        self.assertEqual(output_path,path_output_video)

    # Negative test - send image with invalid file path 
    def test_convert_image_with_invalid_file_path(self):
        with self.assertRaises(ImageConvertError) as ice:
            file_path = r'.\tests\converters\image_to_image\image_none.jpeg'
            ImageConverter(file_path)
        self.assertIn('.\\tests\\converters\\image_to_image\\image_none.jpeg is not a valid image', ice.exception.args[0])
    
    # Negative test - send image with invalid angle rotation (str)
    def test_converter_image_with_invalid_rotation(self):
        with self.assertRaises(ImageConvertError) as ice:
            file_path = r'.\tests\converters\image_to_image\image.jpeg'
            converter = ImageConverter(file_path)
            converter.convert(angle='noveinta grados')
        self.assertIn("Angle must be an integer", ice.exception.args[0])
    
    # Negative test - send image with invalid angle rotation (negative number)
    def test_converter_image_with_invalid_rotation_negative_number(self):
        with self.assertRaises(ImageConvertError) as ice:
            file_path = r'.\tests\converters\image_to_image\image.jpeg'
            converter = ImageConverter(file_path)
            converter.convert(angle=-90)
        self.assertIn("Angle must be positive number.", ice.exception.args[0])
    
    # Negative test - send image with invalid angle rotation (number 361)
    def test_converter_image_with_invalid_rotation_number_361(self):
        with self.assertRaises(ImageConvertError) as ice:
            file_path = r'.\tests\converters\image_to_image\image.jpeg'
            converter = ImageConverter(file_path)
            converter.convert(angle=361)
        self.assertIn("Angle must be a number between [0, 360]", ice.exception.args[0])

    # Negative - Positive test - send image with invalid filter
    def test_converter_image_to_image_with_invalid_filter(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        with self.assertRaises(ImageConvertError) as ice:
            converter = ImageConverter(file_path)
            filters=["Mean Filter"]
            converter.convert(filters=filters)
        self.assertIn("Filter: 'Mean Filter' is not a valid option. Supported options: ['BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SHARPEN', 'SMOOTH', 'SMOOTH_MORE', 'GRAYSCALE'].", ice.exception.args[0])
    
    # Negative test - send image with invalid resize width (str)
    def test_converter_image_to_image_with_invalid_width_str(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ImageConvertError) as ice:
            converter.convert(resize_width='cien',resize_height=1000)
        self.assertIn("Resize width must be an integer.", ice.exception.args[0])
    
    # Negative test - send image with invalid resize width (negative number)
    def test_converter_image_to_image_with_invalid_width_negative_number(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ImageConvertError) as ice:
            converter.convert(resize_width=-1,resize_height=1000)
        self.assertIn("Resize width must be positive number.", ice.exception.args[0])

    # Negative test - send image with invalid resize height (str)
    def test_converter_image_to_image_with_invalid_height_str(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ImageConvertError) as ice:
            converter.convert(resize_width=1000,resize_height='cien')
        self.assertIn("Resize height must be an integer.", ice.exception.args[0])

    # Negative test - send image with invalid resize height (negative number)
    def test_converter_image_to_image_with_invalid_height_negative_number(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ImageConvertError) as ice:
            converter.convert(resize_height=-1)
        self.assertIn("Resize height must be positive number.", ice.exception.args[0])

    #Negative test - send image with invalid resize type
    def test_converter_image_to_image_with_invalid_resize_type(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ImageConvertError) as ice:
            converter.convert(resize_width=600, resize_height = 600,resize_type="INVALID")
        self.assertIn("Resize type: 'INVALID' is not a valid option. Supported options: ['THUMBNAIL', 'COVER', 'FIT', 'PAD'].", ice.exception.args[0])

    # Negative test - send image with invalid output format
    def test_converter_image_to_image_with_invalid_output_format(self):
        file_path = r'.\tests\converters\image_to_image\image.jpeg'
        converter = ImageConverter(file_path)
        with self.assertRaises(ImageConvertError) as ice:
            converter.convert(output_format="mp3")
        self.assertEqual("Output format: 'mp3' is not a valid option. Supported options: ['jpg', 'jpeg', 'png', 'gif'].",ice.exception.args[0])
    

        