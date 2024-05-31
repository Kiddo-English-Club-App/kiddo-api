from flask import Blueprint
from dependify import inject

from shared.id import Id
from theme.application.theme_service import ThemeService
from .dto import ThemeDto

controller = Blueprint('theme', __name__, url_prefix='/themes')


@controller.route('/')
@inject
def get_themes(theme_service: ThemeService):
    return [ThemeDto.from_entity(theme).model_dump() for theme in theme_service.get_themes()]

@controller.route('/<uuid:theme_id>')
@inject
def get_theme(theme_id, theme_service: ThemeService):
    theme =  theme_service.get_theme(Id(theme_id))
    return ThemeDto.from_entity(theme).model_dump()