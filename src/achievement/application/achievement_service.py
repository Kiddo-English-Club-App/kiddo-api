# Achievement service
from uuid import UUID

from achievement.domain.achievement import Achievement
from guest.domain.guest_repository import IGuestRepository
from shared.exceptions import NotFound
from shared.app_context import AppContext, authorize
from ..domain.achievement_repository import IAchievementRepository
from . import dto


class AchievementService:
    
    def __init__(
            self, 
            achievement_repository: IAchievementRepository,
            guest_repository: IGuestRepository,
            app_context: AppContext
            
            ):
        self.achievement_repository = achievement_repository
        self.guest_repository = guest_repository
        self.app_context = app_context

    @authorize("app_context")
    def get_guest_achievements(self, guest_id: UUID, compute: bool = False) -> list[dto.AchievementDto]:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        if compute:
            unlocked = self.compute_achievements(guest_id)
            guest.achievements.extend(unlocked)
            self.guest_repository.save(guest)
                    
        achievements = guest.achievements

        return [dto.AchievementDto.from_entity(achievement) for achievement in achievements]
    
    @authorize("app_context")
    def compute_achievements(self, guest_id: UUID) -> list[Achievement]:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        achievements = [achievement.id for achievement in guest.achievements]
        achievements = self.achievement_repository.find_not_in(achievements)

        unlocked = []

        for achievement in achievements:
            for score in guest.scores:
                if achievement.check(score):
                    unlocked.append(achievement)
                
        return unlocked
