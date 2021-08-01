from os import urandom, getenv


class Config:
    SECRET_KEY = "cyt8745ynt98x34"
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # KV
    KV_ACCOUNT_IDENTIFIER = getenv("KV_ACCOUNT_IDENTIFIER")
    KV_NAMESPACE_IDENTIFIER = getenv("KV_NAMESPACE_IDENTIFIER")
    EMAIL = getenv("EMAIL")
    X_AUTH_KEY = getenv("X_AUTH_KEY")


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"


class TestingConfig(Config):
    ENV = "testing"
    SERVER_NAME = "localhost"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    ENV = "production"
    SECRET_KEY = urandom(24)


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
