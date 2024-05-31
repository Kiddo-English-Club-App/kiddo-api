from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from shared.id import Id


class GuestDto(BaseModel):
    id: UUID
    host: UUID
    name: str
    image: str

    @staticmethod
    def load(guest):
        return GuestDto(
            id=guest.id.value,
            name=guest.name,
            host=guest.host.value,
            image=guest.image
        )

class CreateGuestDto(BaseModel):
    name: str
    image: str
    host: Id

    model_config = ConfigDict(arbitrary_types_allowed=True)


class AchievementDto(BaseModel):
    id: UUID
    value: float
    theme: str
    message: str

    @staticmethod
    def load(achievement):
        return AchievementDto(
            id=achievement.id.value,
            value=achievement.value,
            message=achievement.message,
            theme=achievement.theme
        )


class ScoreDataDto(BaseModel):
    points: float
    time: float
    elements: int
    theme_name: str

    @staticmethod
    def load(score):
        return ScoreDataDto(
            points=score.points,
            time=score.time,
            elements=score.elements,
            theme_name=score.theme_name)


class ReportDto(BaseModel):

    guest_id: UUID
    avg_points: float
    avg_time: float
    top_scores: list[ScoreDataDto]
    bottom_scores: list[ScoreDataDto]

    @staticmethod
    def load(report):
        return ReportDto(
            guest_id=report.guest_id.value,
            avg_points=report.avg_points,
            avg_time=report.avg_time,
            top_scores=[ScoreDataDto.load(score) for score in report.top_scores],
            bottom_scores=[ScoreDataDto.load(score) for score in report.bottom_scores])
    

class AddScoreDto(BaseModel):
    guest_id: Id
    theme_id: Id
    points: int
    time: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("guest_id", "theme_id", mode="plain")
    def validate_id(cls, v):
        return Id(v)


class ScoreDto(BaseModel):
    class ThemeInner(BaseModel):
        id: UUID
    
    guest_id: UUID
    points: float
    time: float
    elements: int
    theme: ThemeInner

    @staticmethod
    def load(score):
        return ScoreDto(
            guest_id=score.guest_id.value,
            points=score.points,
            time=score.time,
            elements=score.elements,
            theme=ScoreDto.ThemeInner(id=score.theme_id.value)
        )