class DomainException(Exception):
    """
    Base class for bussiness errors
    """
    message: str
    title: str
    def __init__(self, message, title = "error"):
        self.message = message
        self.title = title
        super().__init__(message)


class MessageException(DomainException):
    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message, self.title)


class Unauthenticated(MessageException):
    message: str = "Not authenticated"
    title: str = "unauthorized"


class Unauthorized(MessageException):
    message: str = "Forbidden"
    title: str = "forbidden"


class NotFound(MessageException):
    message: str = "Not found"
    title: str = "not_found"


class ValidationError(MessageException):
    message: str = "Validation error"
    title: str = "validation_error"


class InvalidCredentials(MessageException):
    message: str = "Invalid credentials"
    title: str = "invalid_credentials"


class InvalidToken(MessageException):
    message: str = "Invalid token"
    title: str = "invalid_token"


class InvalidPassword(MessageException):
    message: str = "Invalid password"
    title: str = "invalid_password"


class AlreadyExists(MessageException):
    message: str = "Already exists"
    title: str = "already_exists"