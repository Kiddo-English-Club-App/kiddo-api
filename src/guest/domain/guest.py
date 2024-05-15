# Domain model
from uuid import UUID, uuid4

from score.domain.score import Score
from achievement.domain.achievement import Achievement

# TODO: Add achievement list retrieval
class Guest:
    id: UUID
    name: str
    host: UUID
    image: str
    scores: list[Score]
    achievements: list[Achievement]

    def __init__(
            self, 
            name: str, 
            image: str,
            host: UUID, 
            scores: list[Score] = [],
            achievements: list[Achievement] = [],
            id: UUID = uuid4()) -> None:
        self.id = id
        self.name = name
        self.image = image
        self.scores = scores
        self.host = host
        self.achievements = achievements