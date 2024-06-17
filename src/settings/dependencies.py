"""
This module is responsible for initializing the application's dependencies.
It initializes the database connection and the document models.
"""

__data = {}  # Store the database connection, client, and other data


def init(app):
    """
    Initialize the module
    """
    __init_bunnet()
    pass


def __init_bunnet():
    from .environment import env, EnvType
    from bunnet import init_bunnet
    from pymongo import MongoClient

    if env.ENV == EnvType.TESTING:
        env.MONGO_DB_NAME = "kiddo_app_test"

    client = MongoClient(env.MONGO_URI, uuidRepresentation="standard")

    database = client[env.MONGO_DB_NAME]

    __data["db"] = database
    __data["client"] = client

    models = [
        "account.infrastructure.mongo_repository.DBAccount",
        "theme.infrastructure.mongo_repository.DBTheme",
        "player.infrastructure.mongo_guest_repository.DBGuest",
        "player.infrastructure.mongo_achievement_repository.DBAchievement",
    ]
    init_bunnet(database, document_models=models)


def populate_db():
    """
    Populate the database with mock data for testing purposes.

    This method should only be called in the testing environment.
    """
    from .environment import env, EnvType

    if env.ENV != EnvType.TESTING:
        raise Exception("This method should only be called in the testing environment")

    import json
    import bcrypt

    from uuid import UUID

    db = __data["db"]

    with open(env.MOCK_DIR + "/data.json") as f:
        data = json.load(f)

    def replace_id(doc, coll):
        if isinstance(doc, dict):
            if "_id" in doc:
                doc["_id"] = UUID(doc["_id"])

            if "id" in doc:
                doc["id"] = UUID(doc["id"])

            if "theme" in doc:
                doc["theme"] = UUID(doc["theme"])

            match coll:
                case "guests":
                    if "achievements" in doc:
                        doc["achievements"] = [UUID(ach) for ach in doc["achievements"]]

                    if "host" in doc:
                        doc["host"] = UUID(doc["host"])

                case "accounts":
                    if "password" in doc:
                        doc["password"] = bcrypt.hashpw(
                            doc["password"].encode(), bcrypt.gensalt()
                        ).decode()

            for _, value in doc.items():
                replace_id(value, coll)

        if isinstance(doc, list):
            for item in doc:
                replace_id(item, coll)

    for collection, docs in data.items():
        replace_id(docs, collection)
        db[collection].insert_many(docs)


def delete_db():
    from .environment import env, EnvType

    if env.ENV != EnvType.TESTING:
        raise Exception("This method should only be called in the testing environment")

    client = __data["client"]
    db = client[env.MONGO_DB_NAME]
    colls = db.list_collection_names()

    for coll in colls:
        db[coll].delete_many({})
