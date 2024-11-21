from validators.validator import Validator
from validators.int_validator import IntValidator
from validators.validator_context import ValidatorContext

#Validates if the number given is within the length range of the list
class LenValidator(Validator):
    def __init__(self, list, number, param_name):
        super().__init__( param_name)
        self.list = list
        self.number = number
        
    def validate(self):
        validators = [IntValidator(self.number, True, self.param_name)]
        ValidatorContext(validators, self.error_class).run_validations()
        
        list_length = len(self.list) - 1
        if int(self.number) > list_length:
            raise self.error_class(f"{self.param_name} must be <= {list_length}", 400)


