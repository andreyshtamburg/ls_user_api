import os


class Config:
    """
        Flask app config
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ""
    SWAGGER_DOC_PATH = "/doc/"
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")


class DevelopmentConfig(Config):
    user = os.getenv('POSTGRES_USER', 'source')
    pwd = os.getenv('POSTGRES_PASSWORD', 'secret')
    db = os.getenv('POSTGRES_DB', 'source')
    host = 'db'
    port = '5432'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://%s:%s@%s:%s/%s" % (user, pwd, host, port, db)
    # for quick local connect
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://source:secret@localhost/source"
    SWAGGER_UI_DOC_EXPANSION = "list"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""
    SWAGGER_UI_DOC_EXPANSION = "list"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

key = Config.SECRET_KEY
