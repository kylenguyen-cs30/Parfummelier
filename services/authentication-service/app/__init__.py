from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)

    # Define allowed origins
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Single CORS configuration
    CORS(
        app,
        resources={
            r"/*": {
                "origins": ALLOWED_ORIGINS,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "expose_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    @app.before_request
    def log_request_info():
        logger.debug("Headers: %s", dict(request.headers))
        logger.debug("Method: %s", request.method)
        logger.debug("URL: %s", request.url)

    # Debug middleware to log CORS headers
    @app.after_request
    def debug_cors(response):
        print("Request Origin:", request.headers.get("Origin"))
        print("CORS Headers:", dict(response.headers))
        return response

    from app.routes import auth_blueprint

    app.register_blueprint(auth_blueprint)
    return app


def configure_app(app):
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "make-up-key-no-use")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://admin:password@db/capstone_project"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
