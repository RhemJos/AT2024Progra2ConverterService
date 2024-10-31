from image_converter import ImageConverter

if __name__ == '__main__':

    file_path = "/Users/josemarcastro/Downloads/Main Component/Jala University/images/mazda.jpeg"
    file_extension = "png"

    image_converter = ImageConverter(file_path, file_extension)

    image_converter.image_resize()
    image_converter.image_rotate()
    image_converter.image_crop()
    image_converter.image_convert()