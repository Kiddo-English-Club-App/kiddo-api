def init():
    from dependify import register
    from .mongo_repository import MongoDBAchievementRepository, IAchievementRepository

    register(IAchievementRepository, MongoDBAchievementRepository)