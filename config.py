import os

class Config:

    SECRET_KEY = os.environ.get('secret-key')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dominic:12345@localhost/blogs'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}