from PIL import Image
from PIL import ImageFilter
import os

FILTERS = ("BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", 
           "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE")

class ImageConverter:
    def __init__(self, path, extension):
        self.path = path
        self.extension = extension
        self.img = Image.open(self.path)

    def resize(self, measures):
        if (len(measures) != 2):
            raise ValueError("Resize debe ser de tipo (ancho, alto)")
        width = measures[0]
        height = measures[1]
        if not (width):
            width = self.img.width
        if not (height):
            height = self.img.height
        self.img = self.img.resize((width, height))

    def rotate(self, angle):
        self.img = self.img.rotate(angle, expand=True, fillcolor="black")

    def grayscale(self):
        self.img = self.img.convert("L")

    def apply_filter(self, filter_name):
        filter_name = getattr(ImageFilter, filter_name, None)
        if filter_name:
            self.img = self.img.filter(filter_name)

    def convert(self, resize=None, angle=None, grayscale=None, filters=[]):
        if angle:
            self.rotate(angle)
        if grayscale:
            self.grayscale()
        if filters:
            for filter in filters:
                self.apply_filter(filter)
        if resize: 
            self.resize(resize)
        
        base_name = os.path.splitext(os.path.basename(self.path))[0]
        edited_name = f"{base_name}_edited.{self.extension}"
        output_path = os.path.join('outputs', 'image_converted_outputs', edited_name)
        self.img.save(output_path)

        return output_path
    
    # @staticmethod
    # def generate_name():
    #     chars = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
    #     name = "".join(random.choice(chars) for _ in range(10))
    #     return name
