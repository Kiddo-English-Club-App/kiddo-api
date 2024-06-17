def init():
    """
    Initializes the theme module by registering the appropriate implementations
    based on the current environment.
    """
    from dependify import register
    from .mongo_repository import MongoDBThemeRepository, IThemeRepository

    register(IThemeRepository, MongoDBThemeRepository)
