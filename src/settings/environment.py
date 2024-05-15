# Init must be called first to initialize the module

class Environment:
    MONGO_URI: str
    MONGO_DB_NAME: str
    APP_SECRET: str
    ACCESS_TOKEN_SECRET: str
    ACCESS_TOKEN_EXPIRATION: int
    REFRESH_TOKEN_SECRET: str
    REFRESH_TOKEN_EXPIRATION: int

env = Environment()

def init(app):
    import os
    from dotenv import load_dotenv
    load_dotenv()

    env.MONGO_URI = os.getenv("KIDDO_MONGO_URI")
    env.MONGO_DB_NAME = os.getenv("KIDDO_MONGO_DB_NAME")
    env.APP_SECRET = os.getenv("KIDDO_APP_SECRET")
    env.ACCESS_TOKEN_SECRET = os.getenv("KIDDO_ACCESS_TOKEN_SECRET")
    env.ACCESS_TOKEN_EXPIRATION = int(os.getenv("KIDDO_ACCESS_TOKEN_EXPIRATION"))
    env.REFRESH_TOKEN_SECRET = os.getenv("KIDDO_REFRESH_TOKEN_SECRET")
    env.REFRESH_TOKEN_EXPIRATION = int(os.getenv("KIDDO_REFRESH_TOKEN_EXPIRATION"))
    