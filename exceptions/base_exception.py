class Error(Exception):
    # Exception for convertion errors
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def get_message(self):
        return self.message
    
    def get_status_code(self):
        return self.status_code
    