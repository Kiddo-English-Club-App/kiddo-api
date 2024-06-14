def init():
    """
    Initialize the theme application module. This function is called by the application
    when it is starting up to register the theme service with the dependency injection
    container.
    """
    from dependify import register

    from .theme_service import ThemeService

    register(ThemeService)
