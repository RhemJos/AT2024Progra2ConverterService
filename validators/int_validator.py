from validators.validator import Validator


class IntValidator(Validator):
    def __init__(self, number, positive: bool, param_name):
        super().__init__( param_name)
        self.number = number
        self.positive = positive
        
    def validate(self):
        try:
            int(self.number)
        except ValueError:
            raise self.error_class(f"{self.param_name} debe ser un número entero.", 400)
        if self.positive:
            if int(self.number) < 0:
                raise self.error_class(f"{self.param_name} debe ser un número positivo.", 400)


