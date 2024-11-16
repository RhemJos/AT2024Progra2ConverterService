from PIL import Image, ImageFilter, ImageOps
import os
from converters.converter import Converter
from exceptions.image_convert_exception import ImageConvertError
from validators.format_validator import FormatValidator
from validators.range_validator import RangeValidator
from validators.float_validator import FloatValidator
from validators.int_validator import IntValidator
from validators.validator_context import ValidatorContext


IMAGE_OPTIONS = {
    "filter" : ["BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", 
            "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE", "GRAYSCALE"],
    "extension" : ['jpg', 'jpeg', 'png', 'gif'],
    "resize_type": ["THUMBNAIL", "COVER", "FIT", "PAD"]
}


class ImageConverter(Converter):
    def __init__(self, file_path):
        super().__init__(file_path)
        try:
            self.img = Image.open(self.file_path)
        except (IOError):
            raise ImageConvertError("El archivo no es una imagen valida", 400)

    def resize(self, width, height, resize_type=None):
        width = width
        height = height
        if not (width):
            width = self.img.width
        if not (height):
            height = self.img.height
        measures = (width, height)
        if resize_type:
            self.preset_resize(measures, resize_type)
        else:
            self.custom_resize(measures)
        
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
                
    def custom_resize(self, measures):
        self.img = self.img.resize(measures)

    def rotate(self, angle):
        self.img = self.img.rotate(angle, expand=True, fillcolor="black")

    def grayscale(self):
        self.img = self.img.convert("L")

    def apply_filter(self, filter_name):
        filter_name = getattr(ImageFilter, filter_name, None)
        if filter_name:
            self.img = self.img.filter(filter_name)

    def convert(self, **kwargs):
        output_format = kwargs.get('output_format', None)
        resize_width = kwargs.get('resize_width', None)
        resize_height = kwargs.get('resize_height', None)
        resize_type = kwargs.get('resize_type', None)
        angle = kwargs.get('angle', None)
        filters = kwargs.get('filters', None)
        if angle:
            self.rotate(angle)
        if 'GRAYSCALE' in filters:
            self.grayscale()
        if filters:
            for filter in filters:
                self.apply_filter(filter)
        if resize_width or resize_height: 
            self.resize( resize_width, resize_height, resize_type)
        if output_format:
            if output_format not in IMAGE_OPTIONS['extension']:
                raise ImageConvertError("Formato de conversión de imagen no soportado.", 400)
            else:
                self.extension = output_format
        
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        edited_name = f"{base_name}_edited.{self.extension}"
        output_path = os.path.join('outputs', 'image_converted_outputs', edited_name)
        self.img.save(output_path)
        return output_path
    
    def validate_params(self, **kwargs):
        if 'output_format' in kwargs:
            validators = [ FormatValidator(kwargs['output_format'], IMAGE_OPTIONS['extension'], "Output format") ]
        if 'resize_width' in kwargs:
            validators.append(IntValidator(kwargs['resize_width'], True, "Resize width") )
            validators.append(IntValidator(kwargs['resize_height'], True, "Resize height") )
        if 'resize_type' in kwargs:
            validators.append(FormatValidator(kwargs['resize_type'], IMAGE_OPTIONS['resize_type'], "Resize type") )
        if 'angle' in kwargs:
            validators.append(RangeValidator(kwargs['angle'], 0, 360, "Angle") )
        if 'grayscale' in kwargs:
            validators.append(FormatValidator(kwargs['volume'], IMAGE_OPTIONS['volume'], "Volume") )
        if 'speed' in kwargs:
            validators.append(FloatValidator(kwargs['speed'], 1, True, "Speed") )
            validators.append(RangeValidator(kwargs['speed'], 0.5, 2.0, "Speed") )
        
        validator_context = ValidatorContext(validators, ImageConvertError)
        validator_context.run_validations()
    


