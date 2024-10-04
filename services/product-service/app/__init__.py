import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:3000"}},
        methods=[
            "GET",
            "POST",
            "PUT",
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
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "my-default-secret-key")
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import product_blueprint

    app.register_blueprint(product_blueprint, url_prefix="/api")

    return app
