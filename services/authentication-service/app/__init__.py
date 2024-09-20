import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from flask_migrate import Migrate

db = SQLAlchemy()

# PERF: No need for Flask Migrating 🙅
#
# migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # CORS for connection
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:3000"}},
        methods=[
            "GET",
            "POST",
            "DELETE",
            "DELETE",
            "OPTIONS",
        ],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://admin:password@db/capstone_project"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from app.routes import auth_blueprint

    app.register_blueprint(auth_blueprint)
    return app
