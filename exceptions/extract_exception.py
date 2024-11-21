from exceptions.base_exception import Error

class ExtractionError(Error):
    # Exception for audio conversion errors
    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = "Data extraction error: " + message