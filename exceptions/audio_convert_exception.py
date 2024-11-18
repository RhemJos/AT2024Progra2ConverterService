from exceptions.convert_exception import ConvertError

class AudioConvertError(ConvertError):
    # Exception for audio conversion errors
    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = "Audio converter: " + message