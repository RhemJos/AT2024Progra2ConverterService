class ConvertError(Exception):
    # Exception for convertion errors
    def __init__(self, message, status_code, bad_args=None):
        super().__init__(message)
        self.status_code = status_code
        self.bad_args = bad_args
        self.message = message + "con los parametros: " + bad_args if bad_args else message

    def get_message(self):
        return self.message
    
    def get_status_code(self):
        return self.status_code
    