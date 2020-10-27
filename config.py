"""Flask config."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = "GDtfDCFYjD"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = 'files'

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin123@jeevan.cdhnjohiqccx.ap-south-1.rds.amazonaws.com/Youtdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///user_contact_query.sqlite"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
