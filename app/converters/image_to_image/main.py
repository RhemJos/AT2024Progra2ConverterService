from image_converter import ImageConverter

if __name__ == '__main__':

    file_path = "color.jpeg"
    file_extension = "jpeg"

    #params needed -> resize?, width, height, rotate?, angle, grayscale?

    image_converter = ImageConverter(file_path, file_extension)

    image_converter.image_convert()