# Init must be called first to initialize the module

def init(app):
    """
    Initialize the module
    """
    __init_bunnet()
    pass


def __init_bunnet():
    from .environment import env
    from bunnet import init_bunnet
    from pymongo import MongoClient

    client = MongoClient(env.MONGO_URI, uuidRepresentation="standard")
    database = client[env.MONGO_DB_NAME]
    models = [
        "account.infrastructure.mongo_repository.DBAccount",
        "theme.infrastructure.mongo_repository.DBTheme",
        "player.infrastructure.mongo_guest_repository.DBGuest",
        "player.infrastructure.mongo_achievement_repository.DBAchievement",
    ]
    init_bunnet(database, document_models=models)