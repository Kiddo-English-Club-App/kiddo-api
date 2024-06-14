"""
This module contains the controller for the theme module.
The controller provides the endpoints to interact with the theme
service and expose the theme data to the client.

The controller is implemented as a Flask Blueprint, which allows
defining routes and handling HTTP requests. The controller uses
dependency injection to inject the theme service into the controller
methods.
"""

from dependify import inject
from flask import Blueprint
from shared.id import Id

from theme.application.theme_service import ThemeService

from .dto import ThemeDto

controller = Blueprint("theme", __name__, url_prefix="/themes")


@controller.route("/")
@inject
def get_themes(theme_service: ThemeService):
    return [
        ThemeDto.from_entity(theme).model_dump() for theme in theme_service.get_themes()
    ]


@controller.route("/<uuid:theme_id>")
@inject
def get_theme(theme_id, theme_service: ThemeService):
    theme = theme_service.get_theme(Id(theme_id))
    return ThemeDto.from_entity(theme).model_dump()
