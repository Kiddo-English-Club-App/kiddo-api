from typing import Protocol
from dataclasses import dataclass

from shared.id import Id
from ..domain.score import Score
from ..domain.achievement import Achievement
from ..domain.guest import Guest


# Guest DTOs
@dataclass(kw_only=True)
class GuestDto:
    id: Id
    host: Id
    name: str
    image: str

    @staticmethod
    def from_entity(guest: Guest):
        return GuestDto(
            id=guest.id, name=guest.name, host=guest.host, image=guest.image
        )


class CreateGuestDto(Protocol):
    host: Id
    name: str
    image: str


# Score DTOs
@dataclass(kw_only=True)
class ScoreDto:
    guest_id: Id
    points: float
    time: float
    elements: int
    theme_id: Id

    @staticmethod
    def from_entity(score: Score, guest_id: Id):
        return ScoreDto(
            guest_id=guest_id,
            points=score.points.current,
            time=score.time.current,
            elements=score.elements,
            theme_id=score.theme.id,
        )


class AddScoreDto(Protocol):
    guest_id: Id
    theme_id: Id
    points: int
    time: int


@dataclass(kw_only=True)
class ScoreDataDto:
    points: float
    time: float
    elements: int
    theme_name: str

    def from_entity(score: Score):
        return ScoreDataDto(
            points=score.points.current,
            time=score.time.current,
            elements=score.elements,
            theme_name=score.theme.value.name,
        )


@dataclass(kw_only=True)
class ReportDto:
    guest_id: Id
    avg_points: float
    avg_time: float
    top_scores: list[ScoreDataDto]
    bottom_scores: list[ScoreDataDto]


# Achievement DTOs
@dataclass(kw_only=True)
class AchievementDto:
    id: Id
    theme: str
    value: float
    message: str

    @staticmethod
    def from_entity(achievement: Achievement) -> "AchievementDto":
        return AchievementDto(
            id=achievement.id,
            theme=achievement.theme.value.name,
            value=achievement.value,
            message=str(achievement),
        )
