def init():
    from dependify import register
    from .mongo_repository import MongoDBGuestRepository, IGuestRepository

    register(IGuestRepository, MongoDBGuestRepository)