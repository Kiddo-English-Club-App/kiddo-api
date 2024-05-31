# Domain model
from shared.id import Id
from .score import Score
from .achievement import Achievement


class Guest:
    id: Id
    name: str
    host: Id
    image: str
    scores: list[Score]
    achievements: list[Achievement]

    def __init__(
            self, 
            name: str, 
            image: str,
            host: Id, 
            scores: list[Score] = [],
            achievements: list[Achievement] = [],
            id: Id = None) -> None:
        
        self.id = id if isinstance(id, Id) else Id()
        self.name = name
        self.image = image
        self.scores = scores
        self.host = host
        self.achievements = achievements
    
    def get_score_by_theme(self, theme_id: Id):
        for score in self.scores:
            if score.theme.id == theme_id:
                return score
        return None
