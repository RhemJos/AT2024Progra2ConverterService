from validators.validator import Validator


class FloatValidator(Validator):
    def __init__(self, number, digits, positive: bool, param_name):
        super().__init__( param_name)
        self.number = number
        self.digits = digits
        self.positive = positive
        
    def validate(self):
        try:
            float(self.number, self.digits)
        except ValueError:
            raise self.error_class(f"{self.param_name} must be an integer or float", 400)
        if self.positive:
            if float(self.number, self.digits) < 0:
                raise self.error_class(f"{self.param_name} must be a positive number", 400)


