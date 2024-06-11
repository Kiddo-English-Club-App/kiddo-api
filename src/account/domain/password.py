import bcrypt
from shared.exceptions import ValidationError


class Password:

    @classmethod
    def hash(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def validate(cls, password: str):
        if len(password) < 8:
            raise ValidationError("Password must have at least 8 characters")

        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must have at least one digit")

        if not any(char.isupper() for char in password):
            raise ValidationError("Password must have at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValidationError("Password must have at least one lowercase letter")

        if not any(char in "!@#$%^&*()-+" for char in password):
            raise ValidationError("Password must have at least one special character (e.g. !@#$%^&*()-+)")


class PasswordStr(str):

    def __new__(cls, password: str, hashed: bool = False):
        """ If the password is already hashed, we store it as is
        Otherwise, we hash it.
        This way, we allow the Password class to be used in two ways:
        - Password("plain-text-password")
        - Password("hashed-password", hashed=True)
        """
        if isinstance(password, PasswordStr):
            return password
        
        if hashed:
            return super().__new__(cls, password)
        Password.validate(password)
        return super().__new__(cls, Password.hash(password))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return bcrypt.checkpw(other.encode(), self.encode())
        return super().__eq__(other)