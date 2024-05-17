from shared.app_context import AppContext
from shared.exceptions import NotFound
from shared.permissions import SameUserPermission, validate
from theme.domain.theme_repository import IThemeRepository
from ..domain.achievement_repository import IAchievementRepository
from ..domain.guest_repository import IGuestRepository

from . import dto


class ScoreService:

    def __init__(
            self,
            guest_repository: IGuestRepository, 
            theme_repository: IThemeRepository,
            achievement_repository: IAchievementRepository,
            app_context: AppContext
            ) -> None:
        self.theme_repository = theme_repository
        self.guest_repository = guest_repository
        self.achievement_repository = achievement_repository
        self.app_context = app_context
    
    def add_score(self, data: dto.AddScoreDto) -> dto.ScoreDto:
        guest = self.guest_repository.find_by_id(data.guest_id)

        if not guest:
            raise NotFound("Guest not found")

        validate(self.app_context, SameUserPermission(guest.host))    

        theme_ref = self.theme_repository.ref(data.theme_id)

        score = guest.update_score(theme_ref, data.points, data.time)
        achievements = self.achievement_repository.find_not_in([achievement.id for achievement in guest.achievements])
        
        for achievement in achievements:
            if achievement.check(score):
                guest.achievements.append(achievement)
        
        self.guest_repository.save(guest)

        return dto.ScoreDto.from_entity(score, guest.id)
    
    def create_report(self, guest_id: str) -> dto.ScoreDataDto:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        validate(self.app_context, SameUserPermission(guest.host)) 
        
        report = guest.create_report()
        return dto.ReportDto(
            guest_id=guest.id,
            avg_points=report.avg_points,
            avg_time=report.avg_time,
            top_scores=[dto.ScoreDataDto.from_entity(score) for score in report.top_scores],
            bottom_scores=[dto.ScoreDataDto.from_entity(score) for score in report.bottom_scores]
        )

