from uuid import UUID, uuid4


class Id:

    value: UUID

    def __init__(self, value: UUID | str = None) -> None:
        if value is None:
            self.value = uuid4()
        elif isinstance(value, str):
            self.value = UUID(value)
        elif isinstance(value, UUID):
            self.value = value
        else:
            raise ValueError(f"Invalid value for Id {value}")
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Id) and self.value == other.value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"Id({self.value})"