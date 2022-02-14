import os

class Config:

    SECRET_KEY =('secret-key')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dominic:12345@localhost/blogs'
    UPLOADED_PHOTOS_DEST ='app/static/photos'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}