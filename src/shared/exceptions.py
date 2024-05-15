class DomainException(Exception):
    """
    Base class for bussiness errors
    """
    message: str
    title: str
    def __init__(self, message, title = "bad_request"):
        self.message = message
        self.title = title
        super().__init__(message)


class Unauthorized(DomainException):
    message: str = "Unauthorized"
    title: str = "unauthorized"
    def __init__(self, message = "Unauthorized"):
        super().__init__(message, "unauthorized")


class Forbidden(DomainException):
    message: str = "Forbidden"
    title: str = "forbidden"

    def __init__(self, message = "Forbidden"):
        super().__init__(message, "forbidden")


class NotFound(DomainException):
    message: str = "Not found"
    title: str = "not_found"

    def __init__(self, message = "Not found"):
        super().__init__(message, "not_found")


class ValidationError(DomainException):
    message: str = "Validation error"
    title: str = "validation_error"

    def __init__(self, message = "Validation error"):
        super().__init__(message, "validation_error")


class InvalidCredentials(DomainException):
    message: str = "Invalid credentials"
    title: str = "invalid_credentials"
    def __init__(self, message = "Invalid credentials"):
        super().__init__(message, "invalid_credentials")


class InvalidToken(DomainException):
    message: str = "Invalid token"
    title: str = "invalid_token"
    def __init__(self, message = "Invalid token"):
        super().__init__(message, "invalid_token")