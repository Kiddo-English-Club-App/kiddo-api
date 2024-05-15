# Theme MongoDB repository implementation 
from bunnet import Document
from pydantic import Field, BaseModel
from uuid import UUID

from shared.reference import Ref
from ..domain.item import Item
from ..domain.theme import Theme
from ..domain.theme_repository import IThemeRepository, ThemeRef

class DBItem(BaseModel):
    id: UUID
    name: str
    image: str
    sound: str

    @staticmethod
    def from_entity(entity: Item):
        return DBItem(
            id=entity.id,
            name=entity.name,
            image=entity.image,
            sound=entity.sound
        )
    
    def to_entity(self) -> Item:
        return Item(
            id=self.id,
            name=self.name,
            image=self.image,
            sound=self.sound
        )


class DBTheme(Document, Theme):
    id: UUID = Field(alias="_id")
    name: str
    description: str
    image: str
    items: list[DBItem]
    background: str
    
    class Settings:
        name = "themes"
    
    @staticmethod
    def from_entity(entity: Theme):
        return DBTheme(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            image=entity.image,
            items=[DBItem.from_entity(item) for item in entity.items],
            background=entity.background
        )
    
    def to_entity(self) -> Theme:
        return Theme(
            id=self.id,
            name=self.name,
            description=self.description,
            image=self.image,
            items=[item.to_entity() for item in self.items],
            background=self.background
        )


class MongoDBThemeRepository(IThemeRepository):

    def find_by_id(self, id: UUID) -> Theme:
        _theme = DBTheme.find_one({"_id": id}).run()
        if not _theme:
            return None
        return _theme.to_entity()
    
    def find_all(self) -> list[Theme]:
        _themes = DBTheme.find_all().run()
        return [_theme.to_entity() for _theme in _themes]
    
    def save(self, entity: Theme) -> None:
        _theme = DBTheme.from_entity(entity)
        _theme.save()

    def delete_by_id(self, id: UUID) -> bool:
        results = DBTheme.get_motor_collection().delete_one({"_id": id})
        return results.deleted_count > 0
    
    def ref(self, id: UUID) -> Ref[Theme]:
        return ThemeRef(id, self)