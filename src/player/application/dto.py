from uuid import UUID
from pydantic import BaseModel

from ..domain.score import Score
from ..domain.achievement import Achievement
from ..domain.guest import Guest


# Guest DTOs
class GuestDto(BaseModel):
    id: UUID
    host: UUID
    name: str
    image: str

    @staticmethod
    def from_entity(guest: Guest):
        return GuestDto(
            id=guest.id,
            name=guest.name,
            host=guest.host,
            image=guest.image
        )


class CreateGuestDto(BaseModel):
    host: UUID
    name: str
    image: str


# Score DTOs
class ScoreDto(BaseModel):
    guest_id: UUID
    points: float
    time: float
    elements: int
    theme_id: UUID

    @staticmethod
    def from_entity(score: Score, guest_id: UUID):
        return ScoreDto(
            guest_id=guest_id,
            points=score.points.current,
            time=score.time.current,
            elements=score.elements,
            theme_id=score.theme.id
        )


class AddScoreDto(BaseModel):
    guest_id: UUID
    points: int
    time: int
    theme_id: UUID


class ScoreDataDto(BaseModel):
    points: float
    time: float
    elements: int
    theme_name: str

    def from_entity(score: Score):
        return ScoreDataDto(
            points=score.points.current,
            time=score.time.current,
            elements=score.elements,
            theme_name=score.theme.value.name
        )


class ReportDto(BaseModel):
    guest_id: UUID
    avg_points: float
    avg_time: float
    top_scores: list[ScoreDataDto]
    bottom_scores: list[ScoreDataDto]


# Achievement DTOs
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