# Guest MongoDB repository implementation 
from dependify import inject
from bunnet import Document
from pydantic import Field, BaseModel
from uuid import UUID


from shared.range import Range
from theme.domain.theme_repository import IThemeRepository
from ..domain.achievement_repository import IAchievementRepository
from ..domain.guest import Guest, Score
from ..domain.guest_repository import IGuestRepository, Guest


class DBRange(BaseModel):
    current: float = 0.0
    max: float = 0.0
    min: float = 0.0

    def to_range(self) -> Range:
        return Range(
            value=self.current,
            _max=self.max,
            _min=self.min
        )
    
    @staticmethod
    def from_range(range: Range) -> "DBRange":
        return DBRange(
            current=range.current,
            max=range.max,
            min=range.min
        )


class DBScore(BaseModel):
    points: DBRange
    time: DBRange
    elements: int
    theme: UUID

    @inject
    def to_entity(self, theme_repository: IThemeRepository):
        
        return Score(
            points=self.points.to_range(),
            time=self.time.to_range(), 
            elements=self.elements, 
            theme=theme_repository.ref(self.theme))

    @staticmethod
    def from_entity(entity: Score) -> "DBScore":
        points = DBRange.from_range(entity.points)
        time = DBRange.from_range(entity.time)

        return DBScore(
            points=points, 
            time=time, 
            elements=entity.elements, 
            theme=entity.theme.id)  


class DBGuest(Document):
    id: UUID = Field(alias="_id")
    host: UUID
    name: str
    image: str
    scores: list[DBScore]
    achievements: list[UUID]
    
    class Settings:
        name = "guests"

    @inject
    def to_entity(
            self,
            achievement_repository: IAchievementRepository) -> Guest:
        achievements = achievement_repository.find_many(self.achievements)

        return Guest(
            id=self.id,
            host=self.host,
            name=self.name,
            image=self.image,
            scores=[score.to_entity() for score in self.scores],
            achievements=achievements
        )
    
    @staticmethod
    def from_entity(entity: Guest) -> "DBGuest":
        return DBGuest(
            id=entity.id, 
            host=entity.host, 
            name=entity.name, 
            image=entity.image,
            scores=[DBScore.from_entity(score) for score in entity.scores],
            achievements=[achievement.id for achievement in entity.achievements]
        )



class MongoDBGuestRepository(IGuestRepository):

    def find_by_id(self, id: UUID) -> Guest:
        _guest = DBGuest.find_one({"_id": id}).run()
        if not _guest:
            return None
        return _guest.to_entity()
    
    def find_all(self, host: UUID) -> list[Guest]:
        _guests = DBGuest.find({"host": host}).run()
        return [_guest.to_entity() for _guest in _guests]
    
    def save(self, entity: Guest) -> None:
        _guest = DBGuest.from_entity(entity)
        _guest.save()

    def delete_by_id(self, id: UUID) -> bool:
        results = DBGuest.get_motor_collection().delete_one({"_id": id})
        return results.deleted_count > 0