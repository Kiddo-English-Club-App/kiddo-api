from pydantic import BaseModel

from ..domain.item import Item
from ..domain.theme import Theme


class ItemDto(BaseModel):
    id: str
    name: str
    image: str
    sound: str

    @staticmethod
    def from_enitity(item: Item):
        return ItemDto(
            id=str(item.id),
            name=item.name,
            image=item.image,
            sound=item.sound
        )


class ThemeDto(BaseModel):
    id: str
    name: str
    description: str
    image: str
    background: str
    items: list[ItemDto]

    @staticmethod
    def from_entity(theme: Theme):
        return ThemeDto(
            id=str(theme.id),
            name=theme.name,
            description=theme.description,
            image=theme.image,
            background=theme.background,
            items=[ItemDto.from_enitity(item) for item in theme.items]
        )