from exceptions.extract_exception import ExtractionError

class MetadataExtractationError(ExtractionError):
    # Exception for audio conversion errors
    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = "Metadata extractor: " + message