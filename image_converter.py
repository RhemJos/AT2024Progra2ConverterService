from PIL import Image

class ImageConverter:
    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    def image_resize (self):
        img = Image.open(self.path)
        img_resized = img.resize((int(img.width/2), int(img.height/2)), resample = Image.LANCZOS, box=(70,150,500,300))
        img_resized.show()
        #return img_resized
        return print('Image resized successfully')

    def image_rotate (self):
        img = Image.open(self.path)
        img_rotated = img.rotate(angle=60, expand=True, fillcolor="black") #center=(0,0)
        img_rotated.show()
        # return img_rotated
        return print('Image rotated successfully')

    def image_crop (self):
        img = Image.open(self.path)
        img_cropped = img.crop(box = (20,20 ,300,300))
        img_cropped.show()
        # return img_cropped
        return print('Image cropped successfully')

    def image_convert (self):
        img = Image.open(self.path)
        img.save('output.'+self.extension, self.extension)
        img.show()
        return print('Image converted successfully')
