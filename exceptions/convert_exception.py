from exceptions.base_exception import Error

class ConvertError(Error):
    # Exception for convertion errors
    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = "Convertion error: " + message

    