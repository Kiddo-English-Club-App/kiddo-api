from uuid import UUID
from bunnet import Document
from pydantic import Field
from dependify import inject

from theme.domain.theme_repository import IThemeRepository
from ..domain.achievement import Achievement, AchievementFactory
from ..domain.achievement_repository import IAchievementRepository


class DBAchievement(Document):
    id: UUID = Field(alias="_id")
    theme: UUID
    value: float
    key: str

    class Settings:
        name = "achievements"

    @inject
    def to_entity(self, theme_repo: IThemeRepository) -> Achievement:
        return AchievementFactory().create(
            id=self.id,
            theme=theme_repo.ref(self.theme),
            key=self.key,
            value=self.value
        )

    @staticmethod
    def from_entity(entity: Achievement) -> "DBAchievement":
        return DBAchievement(id=entity.id, theme=entity.theme, value=entity.value, key=entity._type())



class MongoDBAchievementRepository(IAchievementRepository):

    def find_all(self) -> list[Achievement]:
        achievements = DBAchievement.find_all().run()
        return [achievement.to_entity() for achievement in achievements]
    
    def save(self, entity: Achievement) -> None:
        DBAchievement.from_entity(entity).save()
    
    def find_by_id(self, id: UUID) -> Achievement:
        achievement = DBAchievement.find_one(id=id).run()
        if not achievement:
            return None
        return achievement.to_entity()
    
    def find_many(self, ids: list[UUID]) -> list[Achievement]:
        achievements = DBAchievement.find({"_id": {"$in": ids}}).run()
        return [achievement.to_entity() for achievement in achievements]
    
    def find_not_in(self, ids: list[UUID]) -> list[Achievement]:
        achievements = DBAchievement.find({"_id": {"$nin": ids}}).run()
        return [achievement.to_entity() for achievement in achievements]
