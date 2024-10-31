from image_converter import ImageConverter

if __name__ == '__main__':

    file_path = "/Users/josemarcastro/Downloads/Main Component/Jala University/images/color.jpeg"
    file_extension = "webp"

    image_converter = ImageConverter(file_path, file_extension)

    image_converter.image_convert()