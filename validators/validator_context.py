
class ValidatorContext():
    def __init__(self, validators: list, error_class):
        self.validators = validators
        self.error_class = error_class

    def run_validations(self):
        for validator in self.validators:
            validator.set_error_class(self.error_class)
            validator.validate()