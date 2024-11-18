from exceptions.convert_exception import ConvertError


class VideoConvertError(ConvertError):
    # Exception for video convertion errors
    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = "Video converter: " + message