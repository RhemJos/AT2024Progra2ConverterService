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
from exceptions.image_convert_exception import ImageConvertError
from validators.format_validator import FormatValidator
from validators.range_validator import RangeValidator
from validators.int_validator import IntValidator
from validators.validator_context import ValidatorContext
from converters.constants import IMAGE_OPTIONS



class ImageConverter(Converter):
    def __init__(self, file_path):
        super().__init__(file_path)
        try:
            self.img = Image.open(self.file_path)
        except (IOError):
            raise ImageConvertError(f"{self.file_path} is not a valid image", 400)

    def resize(self, width, height, resize_type=None):
        width = width
        height = height
        if not (width):
            width = self.img.width
        if not (height):
            height = self.img.height
        measures = (int(width), int(height))
        if resize_type:
            self.__preset_resize(measures, resize_type)
        else:
            self.__custom_resize(measures)
        
    def preset_resize(self, measures, resize_type):
        match resize_type:
            case "THUMBNAIL":
                self.img.thumbnail(measures)      
            case "COVER":
                self.img = ImageOps.cover(self.img, measures)    
            case "FIT":
                self.img = ImageOps.fit(self.img, measures)
            case "PAD":
                self.img = ImageOps.pad(self.img, measures, color="#ffff")    
                
    def __custom_resize(self, measures):
        self.img = self.img.resize(measures)

    def rotate(self, angle):
        self.img = self.img.rotate(int(angle), expand=True, fillcolor="black")

    def __grayscale(self):
        self.img = self.img.convert("L")

    def __apply_filter(self, filter_name):
        filter_name = getattr(ImageFilter, filter_name, None)
        if filter_name:
            self.img = self.img.filter(filter_name)

    def convert(self, **kwargs):
        #validate params
        self.validate_params(**kwargs)

        output_format = kwargs.get('output_format')
        resize_width = kwargs.get('resize_width')
        resize_height = kwargs.get('resize_height')
        resize_type = kwargs.get('resize_type')
        angle = kwargs.get('angle')
        filters = kwargs.get('filters')

        if angle:
            self.rotate(angle)
        if filters:
            if 'GRAYSCALE' in filters:
                self.grayscale()
            for filter in filters:
                self.apply_filter(filter)
        if resize_width or resize_height: 
            self.resize( resize_width, resize_height, resize_type)
        if output_format:
            self.extension = output_format
        
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        edited_name = f"{base_name}_edited.{self.extension}"
        output_path = os.path.join('outputs', 'image_converted_outputs', edited_name)
        self.img.save(output_path)
        return output_path
    
    def validate_params(self, **kwargs):
        output_format = kwargs.get('output_format')
        resize_width = kwargs.get('resize_width')
        resize_height = kwargs.get('resize_height')
        resize_type = kwargs.get('resize_type')
        angle = kwargs.get('angle')
        filters = kwargs.get('filters')
        validators = []
        if output_format:  
            validators.append(FormatValidator(output_format, IMAGE_OPTIONS['extension'], "Output format") )
        if resize_width:
            validators.append(IntValidator(resize_width, True, "Resize width") )
        if resize_height:
            validators.append(IntValidator(resize_height, True, "Resize height") )
        if resize_type:
            validators.append(FormatValidator(resize_type, IMAGE_OPTIONS['resize_type'], "Resize type") )
        if angle:        
            validators.append(IntValidator(angle, True, "Angle"))
            validators.append(RangeValidator(angle, 0, 360, "Angle") )
        if filters:
            for filter in filters:
                validators.append(FormatValidator(filter, IMAGE_OPTIONS['filter'], "Filter") )
        
        validator_context = ValidatorContext(validators, ImageConvertError)
        validator_context.run_validations()
    
