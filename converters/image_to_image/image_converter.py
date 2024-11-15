from PIL import Image, ImageFilter, ImageOps
import os
from converters.converter import Converter
from helpers.utils import get_args

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
        super().__init__(file_path)
        try:
            self.img = Image.open(self.file_path)
        except (IOError):
            raise ValueError("El archivo no es una imagen valida")

    def resize(self, measures, resize_type=None):
        if (len(measures) != 2):
            raise ValueError("Resize debe ser de tipo (ancho, alto)")
        width = measures[0]
        height = measures[1]
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
        if resize_type not in VALID_RESIZE_TYPES:
            raise ValueError("El tipo de resize ingresado no se reconoce")
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

    def convert(self, output_format=None, **kwargs):
        args = get_args(self.parameters, kwargs)
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
                raise ValueError("Formato de conversión de imagen no soportado.")
            else:
                self.extension = output_format
        
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        edited_name = f"{base_name}_edited.{self.extension}"
        output_path = os.path.join('outputs', 'image_converted_outputs', edited_name)
        self.img.save(output_path)

        return output_path
    


