from uuid import UUID
from pydantic import BaseModel

from ..domain.achievement import Achievement


class AchievementDto(BaseModel):
    id: UUID
    theme: str
    value: float
    message: str

    @staticmethod
    def from_entity(achievement: Achievement) -> "AchievementDto":
        return AchievementDto(
            id=achievement.id, 
            theme=achievement.theme.value.name, 
            value=achievement.value,
            message=str(achievement))