from flask import Blueprint
from dependify import inject

from theme.application.theme_service import ThemeService, dto

controller = Blueprint('theme', __name__, url_prefix='/themes')


@controller.route('/')
@inject
def get_themes(theme_service: ThemeService):
    return [theme.model_dump() for theme in theme_service.get_themes()]

@controller.route('/<uuid:theme_id>')
@inject
def get_theme(theme_id: str, theme_service: ThemeService):
    return theme_service.get_theme(theme_id).model_dump()