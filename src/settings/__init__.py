"""
This module is responsible for initializing the application settings.
It initializes the environment, dependencies, error handlers, and logs.
"""


def init(app):
    """
    Initialize the module
    """

    from . import environment, dependencies, error_handlers, logs

    environment.init(app)
    logs.init()
    dependencies.init(app)
    error_handlers.init(app)

    from account import init as account
    from player import init as player
    from theme import init as theme
    from services import init as services

    account()
    player()
    theme()
    services()
