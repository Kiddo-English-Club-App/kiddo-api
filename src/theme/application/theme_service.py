# Theme service
from shared.app_context import AppContext
from shared.exceptions import NotFound
from shared.id import Id
from shared.permissions import AuthenticatedPermission, validate

from ..domain.theme_repository import IThemeRepository
from . import dto


class ThemeService:
    """
    ThemeService provides operations to manage themes in the application.
    """

    def __init__(self, theme_repository: IThemeRepository, context: AppContext) -> None:
        """
        Creates a new instance of ThemeService with the provided theme repository and application context.

        :param theme_repository: An implementation of IThemeRepository to manage themes.
        :param context: An instance of AppContext to provide access to the current user identity and account type.
        """
        self.theme_repository = theme_repository
        self.app_context = context

    def get_themes(self) -> list[dto.ThemeDto]:
        """
        Retrieves all themes in the application. Requires the user to be authenticated.

        :return: A list of ThemeDto objects representing the themes.
        """
        validate(self.app_context, AuthenticatedPermission())
        themes = self.theme_repository.find_all()
        return [dto.ThemeDto.from_entity(theme) for theme in themes]

    def get_theme(self, theme_id: Id) -> dto.ThemeDto:
        """
        Retrieves a theme by its identifier. Requires the user to be authenticated.

        :param theme_id: The identifier of the theme to retrieve.
        :return: A ThemeDto object representing the theme, if found.
        :raises NotFound: If the theme with the specified identifier is not found.
        """
        validate(self.app_context, AuthenticatedPermission())
        theme = self.theme_repository.find_by_id(theme_id)

        if not theme:
            raise NotFound("Theme not found")
        return dto.ThemeDto.from_entity(theme)
