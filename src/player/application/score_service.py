from shared.app_context import AppContext
from shared.exceptions import NotFound
from shared.id import Id
from shared.permissions import SameUserPermission, validate
from theme.domain.theme_repository import IThemeRepository
from ..domain.score import Score
from ..domain.guest_repository import IGuestRepository
from ..domain.report import Report

from . import dto
from .achievement_service import AchievementService


class ScoreService:
    """
    ScoreService provides methods to manage scores in the game. It allows to add scores
    to a guest and create a report of the scores of a guest.

    It validates that the guest exists and that the theme exists.
    """

    def __init__(
        self,
        guest_repository: IGuestRepository,
        theme_repository: IThemeRepository,
        achievement_service: AchievementService,
        app_context: AppContext,
    ) -> None:
        self.theme_repository = theme_repository
        self.guest_repository = guest_repository
        self.achievement_service = achievement_service
        self.app_context = app_context

    def add_score(self, data: dto.AddScoreDto) -> dto.ScoreDto:
        """
        Add a score to a guest. It validates that the guest exists and that the theme exists.
        It also validates that the user is the host of the guest. It updates the score if it already exists.
        Validates the achievements of the guest based on the score.

        :param data: The data to add the score.
        :return: The created or updated score.
        :raises NotFound: If the guest or theme is not found.
        :raises Unauthorized: If the user is not the host of the guest.
        """
        guest = self.guest_repository.find_by_id(data.guest_id)

        if not guest:
            raise NotFound("Guest not found")

        validate(self.app_context, SameUserPermission(guest.host))

        # Check if the theme exists
        theme = self.theme_repository.find_by_id(data.theme_id)
        if not theme:
            raise NotFound("Theme not found")

        theme_ref = self.theme_repository.ref(theme.id)

        # Check if the score already exists
        score = guest.get_score_by_theme(data.theme_id)

        # Create or update the score
        if not score:
            score = Score(theme_ref, data.points, data.time)
            guest.scores.append(score)
        else:
            score.update(data.points, data.time)

        # Validate the achievements of the guest
        achievements = self.achievement_service.validate_guest_achievements(
            guest, score
        )

        # Add the achievements to the guest
        guest.achievements.extend(achievements)

        self.guest_repository.save(guest)

        return dto.ScoreDto.from_entity(score, guest.id)

    def create_report(self, guest_id: Id) -> dto.ReportDto:
        """
        Create a report of the scores of a guest. It validates that the user is the host of the guest.

        :param guest_id: The unique identifier of the guest.
        :return: The report of the scores of the guest.
        :raises NotFound: If the guest is not found.
        :raises Unauthorized: If the user is not the host of the guest.
        """
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")

        validate(self.app_context, SameUserPermission(guest.host))

        report = Report(guest.scores, 3)
        return dto.ReportDto(
            guest_id=guest.id,
            avg_points=report.avg_points,
            avg_time=report.avg_time,
            top_scores=[
                dto.ScoreDataDto.from_entity(score) for score in report.top_scores
            ],
            bottom_scores=[
                dto.ScoreDataDto.from_entity(score) for score in report.bottom_scores
            ],
        )
