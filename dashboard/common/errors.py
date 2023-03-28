from strawberry.exceptions import StrawberryException


class ValidationError(StrawberryException):
    def __init__(self, message: str):
        super().__init__(message)
