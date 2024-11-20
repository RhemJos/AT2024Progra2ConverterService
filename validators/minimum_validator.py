from validators.validator import Validator
from validators.float_validator import FloatValidator
from validators.validator_context import ValidatorContext

class MinimumValidator(Validator):
    def __init__(self, number, min_value, param_name):
        super().__init__( param_name)
        self.number = number
        self.min_value = min_value


    def validate(self):
        validators = [FloatValidator(self.number, True, self.param_name),
                      FloatValidator(self.min_value, True, "Min value")]
        ValidatorContext(validators, self.error_class).run_validations()

        if not (float(self.number) >= float(self.min_value)):
            raise self.error_class(f"{self.param_name} must be >= {self.min_value}", 400)


