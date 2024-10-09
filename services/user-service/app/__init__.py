import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # NOTE: For Development
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
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

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://admin:password@db/capstone_project"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # app config for secret key
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "my-default-secret-key")
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import user_blueprint

    app.register_blueprint(user_blueprint)

    return app


# NOTE: For Deployment

# -----------------------------------------------------------------------#
# CORS(
#     app,
#     resources={r"/*": {"origins": os.getenv("REACT_APP_API_URL")}},
#     methods=[
#         "GET",
#         "POST",
#         "PUT",
#         "DELETE",
#         "OPTIONS",
#     ],
#     supports_credentials=True,
#     allow_headers=[
#         "Content-Type",
#         "Authorization",
#         "Access-Control-Allow-Credentials",
#     ],
# )
# -----------------------------------------------------------------------#
