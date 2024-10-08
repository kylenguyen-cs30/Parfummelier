from flask import Flask
from .routes import forum_blueprint


def create_app():
    app = Flask(__name__)

    # Register routes for API
    app.register_blueprint(forum_blueprint)

    return app
