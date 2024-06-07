from shared.exceptions import ValidationError


class NameStr(str):

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
        