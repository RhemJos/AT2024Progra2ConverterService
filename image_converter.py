import string
from PIL import Image
from PIL.ImagePalette import random
import random

class ImageConverter:
    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    def image_resize (self, path):
        img = Image.open(path)
        img_resized = img.resize((int(img.width/2), int(img.height/2)), box=(20,20,300,300))
        name = self.generate_name()
        img_resized.save('Resize/'+name+'.png')
        file_path = 'Resize/'+name+'.png'
        return file_path

    def image_rotate (self, path):
        img = Image.open(path)
        img_rotated = img.rotate(angle=60, expand=True, fillcolor="black") #center=(0,0)
        name = self.generate_name()
        img_rotated.save('Rotate/'+name+'.png')
        file_path = 'Rotate/'+name+'.png'
        return file_path

    def image_grayscale (self, path):
        img = Image.open(path)
        img_grayscaled = img.convert("L")
        name = self.generate_name()
        img_grayscaled.save('Grayscale/'+name+'.png')
        file_path = 'Grayscale/'+name+'.png'
        return file_path

    #def image_crop (self, file):
    #    img = Image.open(file)
    #    img_cropped = img.crop(box = (20,20 ,300,300))
    #    return img_cropped

    def image_convert (self):
        resized = self.image_resize(self.path)
        rotated = self.image_rotate(resized)
        grayscale = self.image_grayscale(rotated)
        name = self.generate_name()
        img_converted = Image.open(grayscale)
        print(self.extension)
        img_converted.convert("RGB")
        img_converted.save('Output/'+name+'.'+self.extension, format = self.extension)
        file_path = 'Output/'+name+'.'+self.extension
        print('Image converted successfully '+ file_path)
        return file_path


    @staticmethod
    def generate_name ():
        chars = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
        name = ""
        for i in range (10):
            name += random.choice(chars)
        return name
