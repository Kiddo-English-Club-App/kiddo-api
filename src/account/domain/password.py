import bcrypt
from shared.exceptions import InvalidPassword


class Password:
    hashed: str

    def __init__(self, password: str, hashed: bool = False):
        # If the password is already hashed, we store it as is
        # Otherwise, we hash it
        # This way, we allow the Password class to be used in two ways:
        # - Password("plain-text-password")
        # - Password("hashed-password", hashed=True)
        if hashed:
            self.hashed = password
        else:
            self.validate(password)
            self.hashed = self._hash(password)

    def _hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Password):
            return self.hashed == other.hashed

        if isinstance(other, str):
            return bcrypt.checkpw(other.encode(), self.hashed.encode())

        return False

    def validate(self, password: str):
        if len(password) < 8:
            raise InvalidPassword("Password must have at least 8 characters")

        if not any(char.isdigit() for char in password):
            raise InvalidPassword("Password must have at least one digit")

        if not any(char.isupper() for char in password):
            raise InvalidPassword("Password must have at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise InvalidPassword("Password must have at least one lowercase letter")

        if not any(char in "!@#$%^&*()-+" for char in password):
            raise InvalidPassword("Password must have at least one special character (e.g. !@#$%^&*()-+)")
