# Domain model
from shared.id import Id
from .item import Item


class Theme:
    id: Id
    name: str
    description: str
    image: str
    items: list[Item]
    background: str

    def __init__(
            self, 
            name: str, 
            description: str, 
            image: str, 
            background: str,
            items: list[Item] = [],
            id: Id = None 
            ):
        
        self.id = id if isinstance(id, Id) else Id()
        self.name = name
        self.description = description
        self.image = image
        self.items = items
        self.background = background

    
    def add_item(self, item: Item):
        self.items.append(item)
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Theme) and value.id == self.id