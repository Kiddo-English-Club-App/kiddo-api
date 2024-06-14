from dataclasses import dataclass

from shared.id import Id

from ..domain.item import Item
from ..domain.theme import Theme


@dataclass(kw_only=True)
class ItemDto:
    """
    ItemDto is a data transfer object that represents an item in the theme application.
    """

    id: Id
    name: str
    image: str
    sound: str

    @staticmethod
    def from_enitity(item: Item):
        return ItemDto(id=item.id, name=item.name, image=item.image, sound=item.sound)


@dataclass(kw_only=True)
class ThemeDto:
    """
    ThemeDto is a data transfer object that represents a theme in the theme application module.
    """

    id: Id
    name: str
    description: str
    image: str
    background: str
    items: list[ItemDto]

    @staticmethod
    def from_entity(theme: Theme):
        return ThemeDto(
            id=theme.id,
            name=theme.name,
            description=theme.description,
            image=theme.image,
            background=theme.background,
            items=[ItemDto.from_enitity(item) for item in theme.items],
        )
