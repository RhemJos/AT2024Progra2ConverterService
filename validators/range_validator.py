from validators.validator import Validator

class RangeValidator(Validator):
    def __init__(self, number, left_limit, right_limit, param_name):
        super().__init__( param_name)
        self.number = number
        self.left_limit = left_limit
        self.right_limit = right_limit


    def validate(self):
        try:
            self.number = float(self.number)
            self.left_limit = float(self.left_limit)
            self.right_limit = float(self.right_limit)
        except ValueError:
            raise self.error_class(f"{self.param_name} and range values must be numbers", 400)

        if not (self.left_limit <= self.number <= self.right_limit):
            raise self.error_class(f"{self.param_name} must be a number between [{self.left_limit}, {self.right_limit}]", 400)


