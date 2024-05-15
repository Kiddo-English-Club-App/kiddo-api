from uuid import UUID, uuid4


class Item:
    id: UUID
    name: str
    image: str
    sound: str

    def __init__(self, name: str, image: str, sound: str, id: UUID = uuid4()):
        self.id = id
        self.name = name
        self.image = image
        self.sound = sound

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Item) and value.id == self.id