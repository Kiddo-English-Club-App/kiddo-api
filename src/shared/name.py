from shared.exceptions import ValidationError


class NameStr(str):
    """
    NameStr is a value object that represents a name. It can be initialized with a string value. It 
    can be compared for equality with other NameStr objects. It extends the str class and adds validation
    for the name value. 

    NameStr objects are immutable and should be created using the class constructor.

    A name must follow these rules:
    - It must be at least 2 characters long.
    - It must be at most 50 characters long.
    - It must contain only alphabetic characters.
    - It must be title cased.
    """

    def __new__(cls, value, *args, **kwargs):
        n_value = value.strip()
        cls._validate(n_value)
        return super().__new__(cls, n_value)
    
    @classmethod
    def _validate(cls, value: str) -> None:
        if len(value) < 2:
            raise ValidationError(f"Name must be at least 2 characters long: {len(value)}")
        if len(value) > 50:
            raise ValidationError(f"Name must be at most 50 characters long: {len(value)}")
        if not value.isalpha():
            raise ValidationError(f"Name must contain only alphabetic characters: {value}")
        if not value.istitle():
            raise ValidationError(f"Name must be title cased: {value}")
        