from flask import Flask

from .routes import server
from .extensions import db


def create_app():
    """ Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    with app.app_context():
        # including routes
        app.register_blueprint(server)
        db.init_app(app)

        return app
