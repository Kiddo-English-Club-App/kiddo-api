def init():
    from dependify import register
    from .mongo_repository import MongoDBThemeRepository, IThemeRepository

    register(IThemeRepository, MongoDBThemeRepository)

