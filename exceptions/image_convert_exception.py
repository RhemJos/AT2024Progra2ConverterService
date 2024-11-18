from exceptions.convert_exception import ConvertError


class ImageConvertError(ConvertError):
    # Exception for image convertion errors
    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = "Image converter: " + message