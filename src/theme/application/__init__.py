def init():
    from dependify import register

    from .theme_service import ThemeService

    register(ThemeService)