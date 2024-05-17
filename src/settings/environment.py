# Init must be called first to initialize the module
from enum import StrEnum


class EnvType(StrEnum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"

class Environment:
    MONGO_URI: str
    MONGO_DB_NAME: str
    APP_SECRET: str
    ACCESS_TOKEN_SECRET: str
    ACCESS_TOKEN_EXPIRATION: int
    REFRESH_TOKEN_SECRET: str
    REFRESH_TOKEN_EXPIRATION: int
    ENV: EnvType
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_KEY: str
    S3_REGION_NAME: str
    S3_BUCKET_NAME: str

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
    env.ENV = EnvType(os.getenv("KIDDO_ENV"))
    env.S3_ENDPOINT_URL = os.getenv("KIDDO_S3_ENDPOINT_URL")
    env.S3_ACCESS_KEY_ID = os.getenv("KIDDO_S3_ACCESS_KEY_ID")
    env.S3_SECRET_KEY = os.getenv("KIDDO_S3_SECRET_KEY")
    env.S3_REGION_NAME = os.getenv("KIDDO_S3_REGION_NAME")
    env.S3_BUCKET_NAME = os.getenv("KIDDO_S3_BUCKET_NAME")
    