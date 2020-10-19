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
    WKHTMLTOPDF_USE_CELERY = True
    WKHTMLTOPDF_CMD_OPTIONS = {
        'quiet': False,
    }
    # The URL to access a webpage download in PDF format
    PDF_URL_RULE = '/<path:path>.pdf'

    # The path and options for wkhtmltopdf executation.
    # `{url}` will be replaced by the url of the page to transform
    # and `{output}` will be a temporary output file (auto-deleted).
    PDF_WKHTMLTOPDF_COMMAND = 'wkhtmltopdf --print-media-type {url} {output}'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///user_contact_query.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
