from ..domain.score import Score
from ..domain.achievement import Achievement
from ..domain.achievement_repository import IAchievementRepository
from ..domain.guest import Guest


class AchievementService:
    """
    AchievementService provides methods to manage achievements in the game.

    It allows to get all achievements and validate the achievements of a guest based on its score.
    """

    def __init__(self, achievements_repository: IAchievementRepository) -> None:
        self.achievements_repository = achievements_repository

    def get_achievements(self) -> list[Achievement]:
        """
        Get all achievements in the game.

        :return: A list of achievements.
        """
        return self.achievements_repository.find_all()

    def validate_guest_achievements(
        self, guest: Guest, score: Score
    ) -> list[Achievement]:
        """
        Validate the achievements of a guest based on its score. It checks if the guest has
        achieved any new achievements based on the score.

        :param guest: The guest to validate the achievements.
        :param score: The score of the guest.
        :return: A list of achievements that the guest has achieved
        """
        achievements = self.achievements_repository.find_not_in(
            [achievement.id for achievement in guest.achievements]
        )

        # Check if the achievement is valid for the guest and if it's not already achieved
        def check_achievement(
            achievement: Achievement, guest: Guest, score: Score
        ) -> bool:
            return achievement.check(score) and achievement not in guest.achievements

        return [
            achievement
            for achievement in achievements
            if check_achievement(achievement, guest, score)
        ]
