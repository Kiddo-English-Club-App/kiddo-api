# Domain model
from uuid import UUID, uuid4

from shared.reference import Ref
from .score import Score, Theme
from .achievement import Achievement
from .report import Report


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

    def update_score(self, theme: Ref[Theme], points: int, time: float) -> None:
        score = self.get_score_by_theme(theme.id)
        if score:
            score.update(points, time)
        else:
            score = Score(theme, points, time)
            self.scores.append(score)
        return score
    
    def get_score_by_theme(self, theme_id: UUID):
        for score in self.scores:
            if score.theme.id == theme_id:
                return score
        return None

    def update_achievements(self, achievements: list[Achievement]) -> None:
        for achievement in achievements:
            if self.check_achievement(achievement):
                self.achievements.append(achievement)

    def create_report(self, number: int = 3) -> Report:
        scores = self.scores.copy()
        avg_points = sum([score.points.current for score in scores])/len(scores)
        avg_time = sum([score.time.current for score in scores])/len(scores)

        scores.sort(key=lambda x: x.points.current, reverse=True)
        
        top_scores = scores[:number]
        bottom_scores = scores[-number:]

        return Report(avg_time, avg_points, top_scores, bottom_scores)