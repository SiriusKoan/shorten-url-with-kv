from os import urandom


class Config:
    SECRET_KEY = "cyt8745ynt98x34"


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    SECRET_KEY = urandom(24)


configs = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}
