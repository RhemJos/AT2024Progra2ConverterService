from validators.validator import Validator
from validators.float_validator import FloatValidator
from validators.validator_context import ValidatorContext

class RangeValidator(Validator):
    def __init__(self, number, left_limit, right_limit, param_name):
        super().__init__( param_name)
        self.number = number
        self.left_limit = left_limit
        self.right_limit = right_limit

    def validate(self):

        validators = [
            FloatValidator(self.number, True, self.param_name),
            FloatValidator(self.left_limit, True, "Left limit"),
            FloatValidator(self.right_limit, True, "Right limit")
        ]
        ValidatorContext(validators, self.error_class).run_validations()

        if not (float(self.left_limit) <= float(self.number) <= float(self.right_limit)):
            raise self.error_class(f"{self.param_name} must be a number between [{self.left_limit}, {self.right_limit}]", 400)


