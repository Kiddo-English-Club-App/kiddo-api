from uuid import UUID
from pydantic import BaseModel

from .application import dto


class ItemDto(BaseModel):
    id: UUID
    name: str
    image: str
    sound: str

    @staticmethod
    def from_entity(item: dto.Item):
        return ItemDto(
            id=item.id.value,
            name=item.name,
            image=item.image,
            sound=item.sound
        )


class ThemeDto(BaseModel):
    id: UUID
    name: str
    description: str
    image: str
    background: str
    items: list[ItemDto]

    @staticmethod
    def from_entity(theme: dto.Theme):
        return ThemeDto(
            id=theme.id.value,
            name=theme.name,
            description=theme.description,
            image=theme.image,
            background=theme.background,
            items=[ItemDto.from_entity(item) for item in theme.items]
        )