# Domain model
from uuid import UUID, uuid4

from .item import Item


class Theme:
    id: UUID
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
            id: UUID = uuid4() 
            ):
        
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.items = items
        self.background = background

    
    def add_item(self, item: Item):
        self.items.append(item)
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Theme) and value.id == self.id