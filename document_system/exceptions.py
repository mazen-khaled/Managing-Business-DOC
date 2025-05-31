class ValidationError(Exception):
    pass

class MissingFieldError(ValidationError):
    pass

class ItemValidationError(ValidationError):
    pass

class AmountExceededError(ValidationError):
    pass