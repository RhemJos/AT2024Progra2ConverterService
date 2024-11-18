from validators.validator import Validator


class FloatValidator(Validator):
    def __init__(self, number, positive: bool, param_name):
        super().__init__( param_name)
        self.number = number
        self.positive = positive
        
    def validate(self):
        try:
            float(self.number)
        except ValueError:
            raise self.error_class(f"{self.param_name} must be a number", 400)
        if self.positive:
            if float(self.number) < 0:
                raise self.error_class(f"{self.param_name} must be a positive number", 400)


