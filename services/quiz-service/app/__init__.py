from flask import Flask, jsonify
from flask_cors import CORS
from .routes import quiz_blueprint

def create_app():
    app = Flask(__name__)

    # Configure CORS for development
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    )

    # Register blueprints
    app.register_blueprint(quiz_blueprint, url_prefix="/quiz")

    # Define a root route
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Quiz Service launched"}), 200

    return app
