from PIL import Image
from PIL.ImagePalette import random
import os

class ImageConverter:
    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    def image_resize(self, width=None, height=None):
        img = Image.open(self.path)
        if width is None or height is None:
            width = img.width
            height = img.height
        img_resized = img.resize((width, height))
        return img_resized

    def image_rotate(self, img, angle):
        img_rotated = img.rotate(angle, expand=True, fillcolor="black")
        return img_rotated

    def image_grayscale(self, img, apply):
        if apply:
            img_grayscaled = img.convert("L")
            return img_grayscaled
        return img

    def image_convert(self, resize=None, rotate=None, grayscale=None):
        img = self.image_resize()

        if rotate is not None:
            img = self.image_rotate(img, rotate)
        
        img = self.image_grayscale(img, grayscale)

        base_name = os.path.splitext(os.path.basename(self.path))[0]
        edited_name = f"{base_name}_edited.{self.extension}"
        output_path = os.path.join('outputs', 'image_converted_outputs', edited_name)
        img.save(output_path)

        return output_path
    
    # @staticmethod
    # def generate_name():
    #     chars = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
    #     name = "".join(random.choice(chars) for _ in range(10))
    #     return name
