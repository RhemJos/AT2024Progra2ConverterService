from validators.Validator import Validator


class FormatValidator(Validator):
    def __init__(self, entered_format, valid_options: list, param_name):
        super().__init__( param_name)
        self.entered_format = entered_format
        self.valid_options = valid_options

    def validate(self):
        if self.entered_format not in self.valid_options:  
            message = f"{self.param_name}: '{self.entered_format}' is not a valid option. Supported options: {self.valid_options}."
            raise self.error_class( message, 400)