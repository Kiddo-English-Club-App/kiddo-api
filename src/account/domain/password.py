import bcrypt
from shared.exceptions import ValidationError


class Password:
    """
    Password class provides utility functions for hashing and validating passwords.
    """

    @classmethod
    def hash(cls, password: str) -> str:
        """
        Hashes the provided password using the bcrypt algorithm.

        :param password: The password to hash.
        :return: A string containing the hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def validate(cls, password: str):
        """
        Validates the provided password against the following criteria:
        - At least 8 characters long
        - Contains at least one digit
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one special character

        :param password: The password to validate.
        :raises ValidationError: If the password does not meet the criteria.
        """
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
    """
    PasswordStr is a custom string class that represents a hashed password. It extends the built-in str class
    and adds additional functionality for password hashing and validation. It ensures that passwords are hashed
    before being stored in the database and provides a way to compare plain-text passwords with their hashed versions.
    """

    def __new__(cls, password: str, hashed: bool = False):
        """ If the password is already hashed, we store it as is, otherwise, we hash it.
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