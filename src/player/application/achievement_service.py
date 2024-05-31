from ..domain.score import Score
from ..domain.achievement import Achievement
from ..domain.achievement_repository import IAchievementRepository
from ..domain.guest import Guest


class AchievementService:

    def __init__(self, achievements_repository: IAchievementRepository) -> None:
        self.achievements_repository = achievements_repository

    def get_achievements(self) -> list[Achievement]:
        return self.achievements_repository.find_all()
    
    def validate_guest_achievements(self, guest: Guest, score: Score) -> list[Achievement]:
        achievements = self.achievements_repository.find_not_in(
            [achievement.id for achievement in guest.achievements])

        def check_achievement(achievement: Achievement, guest: Guest, score: Score) -> bool:
            return achievement.check(score) and achievement not in guest.achievements
        
        return [achievement for achievement in achievements 
                if check_achievement(achievement, guest, score)]
