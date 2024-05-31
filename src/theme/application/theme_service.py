# Theme service
from shared.id import Id
from shared.app_context import AppContext
from shared.exceptions import NotFound
from shared.permissions import AuthenticatedPermission, validate
from ..domain.theme_repository import IThemeRepository
from . import dto


class ThemeService:

    def __init__(self, theme_repository: IThemeRepository, context: AppContext) -> None:
        self.theme_repository = theme_repository
        self.app_context = context

    def get_themes(self) -> list[dto.ThemeDto]:
        validate(self.app_context, AuthenticatedPermission())
        themes = self.theme_repository.find_all()
        return [dto.ThemeDto.from_entity(theme) for theme in themes]

    def get_theme(self, theme_id: Id) -> dto.ThemeDto:
        validate(self.app_context, AuthenticatedPermission())
        theme = self.theme_repository.find_by_id(theme_id)

        if not theme:
            raise NotFound("Theme not found")
        return dto.ThemeDto.from_entity(theme)