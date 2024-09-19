import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # CORS configurations

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://admin:password@db/capstone_project"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import user_blueprint

    app.register_blueprint(user_blueprint)

    return app
