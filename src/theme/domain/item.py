from shared.id import Id


class Item:
    id: Id
    name: str
    image: str
    sound: str

    def __init__(self, name: str, image: str, sound: str, id: Id = None):
        self.id = id if isinstance(id, Id) else Id(id)
        self.name = name
        self.image = image
        self.sound = sound

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Item) and value.id == self.id