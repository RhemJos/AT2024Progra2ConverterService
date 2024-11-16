from validators.validator import Validator


class RangeValidator(Validator):
    def __init__(self, number, left_limit, right_limit, param_name):
        super().__init__( param_name)
        self.number = number
        self.left_limit = left_limit
        self.right_limit = right_limit
        
    def validate(self):
        if not (self.left_limit <= self.number  <= self.right_limit):
            raise self.error_class(f"{self.param_name} must be a number between [{self.left_limit}, {self.right_limit}]", 400)


