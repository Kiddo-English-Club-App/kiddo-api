# Theme service
from uuid import UUID

from shared.app_context import AppContext, authorize
from shared.exceptions import NotFound
from ..domain.theme_repository import IThemeRepository
from . import dto


class ThemeService:

    def __init__(self, theme_repository: IThemeRepository, context: AppContext) -> None:
        self.theme_repository = theme_repository
        self.app_context = context

    @authorize("app_context", "theme:list")
    def get_themes(self) -> list[dto.ThemeDto]:
        themes = self.theme_repository.find_all()
        return [dto.ThemeDto.from_entity(theme) for theme in themes]

    @authorize("app_context", "theme:read")
    def get_theme(self, theme_id: UUID) -> dto.ThemeDto:
        
        theme = self.theme_repository.find_by_id(theme_id)

        if not theme:
            raise NotFound("Theme not found")
        return dto.ThemeDto.from_entity(theme)