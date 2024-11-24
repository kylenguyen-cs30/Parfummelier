# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure CORS
    CORS(
        app,
        resources={
            r"/*": {
                "origins": app.config["CORS_ORIGINS"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "expose_headers": ["Content-Type", "Authorization"],
                "max_age": 600,
                "send_wildcard": False,
            }
        },
    )

    # Register blueprints
    from app.routes import user_blueprint, test_bp

    app.register_blueprint(user_blueprint)
    app.register_blueprint(test_bp, url_prefix="/test")

    return app
