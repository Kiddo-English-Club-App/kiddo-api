# Score service
from uuid import UUID

from shared.exceptions import NotFound
from theme.domain.theme_repository import IThemeRepository
from guest.domain.guest_repository import IGuestRepository
from ..domain.score import Score

from . import dto


class ScoreService:

    def __init__(
            self,
            guest_repository: IGuestRepository, 
            theme_repository: IThemeRepository
            ) -> None:
        self.theme_repository = theme_repository
        self.guest_repository = guest_repository
    
    def add_score(self, data: dto.AddScoreDto) -> dto.ScoreDto:
        guest = self.guest_repository.find_by_id(data.guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        score = None

        for _score in guest.scores:
            if _score.theme.id == data.theme_id:
                print("score found")
                _score.add(data.points, data.time)
                self.guest_repository.save(guest)
                score = _score
                break
        
        if not score:
            score = Score(
                points=data.points,
                time=data.time,
                theme=self.theme_repository.ref(data.theme_id),
                elements=1
            )

            guest.scores.append(score)
            self.guest_repository.save(guest)
        
        return dto.ScoreDto.from_entity(score, guest.id)
    
    def create_report(self, guest_id: UUID, number: int = 3) -> dto.ReportDto:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")

        scores = guest.scores

        if len(scores) == 0:
            return dto.ReportDto(
                guest_id=guest_id,
                avg_points=0,
                avg_time=0,
                top_scores=[],
                bottom_scores=[]
            )
    
        number = min(number, len(scores))
        
        avg_points = sum([score.points for score in scores])/len(scores)
        avg_time = sum([score.time for score in scores])/len(scores)
        
        scores.sort(key=lambda x: x.points, reverse=True)
        
        top_scores = scores[:number]
        bottom_scores = scores[-number:]

        return dto.ReportDto(
            guest_id=guest_id,
            avg_points=avg_points,
            avg_time=avg_time,
            top_scores=[dto.ScoreDataDto.from_entity(score) for score in top_scores],
            bottom_scores=[dto.ScoreDataDto.from_entity(score) for score in bottom_scores]
        )
