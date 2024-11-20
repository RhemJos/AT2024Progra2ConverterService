#
# @image_converter.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from PIL import Image, ImageFilter, ImageOps
import os
from converters.converter import Converter
from helpers.utils import get_args
# Constants for valid image extensions and resize types
IMAGE_FILTERS = ("BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", 
                 "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE")

VALID_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

VALID_RESIZE_TYPES = ("THUMBNAIL", "COVER", "FIT", "PAD")


class ImageConverter(Converter):
    parameters = {
            'resize' : None,
            'resize_type' : None,
            'output_format' : None,
            'angle' : None,
            'grayscale' : None,
            'filters' : None,
        }
    
    def __init__(self, file_path):
        super().__init__(file_path)  # Initialize base class
        try:
            self.img = Image.open(self.file_path)  # Open the image using Pillow
        except (IOError):
            raise ValueError("The file is not a valid image")  # Raise error if not a valid image

    def resize(self, measures, resize_type=None):  # This method resizes the image based on the provided dimensions
        if (len(measures) != 2):
            raise ValueError("Resize must be of type (width, height)")
        width = measures[0]
        height = measures[1]
        if not (width):
            width = self.img.width
        if not (height):
            height = self.img.height
        measures = (width, height)
        if resize_type:  # If the resize_type is provided, it uses one of the preset resizing options
            self.preset_resize(measures, resize_type)
        else:  # otherwise, it uses custom resizing.
            self.custom_resize(measures)
        
    def preset_resize(self, measures, resize_type):  # This method applies one of the preset resizing operations
        if resize_type not in VALID_RESIZE_TYPES:
            raise ValueError("The resize type entered is not recognized")
        match resize_type:
            case "THUMBNAIL":
                self.img.thumbnail(measures)      
            case "COVER":
                self.img = ImageOps.cover(self.img, measures)    
            case "FIT":
                self.img = ImageOps.fit(self.img, measures)
            case "PAD":
                self.img = ImageOps.pad(self.img, measures, color="#ffff")    
                
    def custom_resize(self, measures):  #  This method resizes the image to the custom dimensions provided
        self.img = self.img.resize(measures)

    def rotate(self, angle):  # This method rotates the image by the specified angle, fills empty areas with black color
        self.img = self.img.rotate(angle, expand=True, fillcolor="black")

    def grayscale(self):  # This method converts the image to grayscale using Pillow’s method with the "L" mode
        self.img = self.img.convert("L")

    def apply_filter(self, filter_name):  # This method applies an image filter
        filter_name = getattr(ImageFilter, filter_name, None)
        if filter_name:
            self.img = self.img.filter(filter_name)

    def convert(self, **kwargs):
        args = get_args(self.parameters, kwargs)  # Helper function to get arguments
        resize = args['resize']
        resize_type = args['resize_type']
        output_format = args['output_format']
        angle = args['angle']
        grayscale = args['grayscale']
        filters = args['filters']
        
        if angle:
            self.rotate(angle)
        if grayscale:
            self.grayscale()
        if filters:
            for filter in filters:
                self.apply_filter(filter)
        if resize: 
            self.resize(resize, resize_type)
        if output_format:
            if output_format not in VALID_IMAGE_EXTENSIONS:
                raise ValueError("Image conversion format not supported.")
            else:
                self.extension = output_format
        
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        edited_name = f"{base_name}_edited.{self.extension}"
        output_path = os.path.join('outputs', 'image_converted_outputs', edited_name)
        self.img.save(output_path)  # Save the edited image

        return output_path  # Return the output path where the image is saved
