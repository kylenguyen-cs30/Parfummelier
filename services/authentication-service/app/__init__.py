import os

# from app.routes import login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from flask_login import LoginManager


# from flask_migrate import Migrate

db = SQLAlchemy()
# login_manager = LoginManager()

# PERF: No need for Flask Migrating 🙅
#
# migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Load Configurations
    configure_app(app)

    # initialize extensions
    db.init_app(app)

    # CORS for connection
    CORS(
        app,
        resources={
            r"/*": {"origins": ["http://108.225.73.225", "http://localhost:3000"]}
        },
        methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ],
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
    )

    # @app.before_request
    # def handle_options_request():
    #     if request.method == "OPTIONS":
    #         response = jsonify()
    #         response.headers.add("Access-Control-Allow-Origin", "*")
    #         response.headers.add(
    #             "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
    #         )
    #         response.headers.add(
    #             "Access-Control-Allow-Headers", "Authorization, Content-Type"
    #         )
    #         response.headers.add("Access-Control-Allow-Credentials", "true")
    #         return response, 200

    from app.routes import auth_blueprint

    app.register_blueprint(auth_blueprint)
    return app


def configure_app(app):
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "make-up-key-no-use")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://admin:password@db/capstone_project"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
