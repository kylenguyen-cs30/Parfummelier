from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from pymongo import MongoClient

# from app.forum_blueprint.routes import forum_blueprint

import os

# Initialize SocketIO
socketio = SocketIO()

# NOTE: Set up MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = client["chat_database"]  # This is the database name
chatrooms_collection = db["chatrooms"]  # Chatrooms collection
messages_collection = db["messages"]  # Messages collection


def create_app():
    # Specify the static folder where your frontend files are located
    app = Flask(__name__)
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:3000/"}},
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

    # Register the forum blueprint
    # app.register_blueprint(forum_blueprint, url_prefix="/forum")

    # Register the chat blueprint
    from app.chat_route.routes import chat_blueprint, init_socketio

    app.register_blueprint(chat_blueprint, url_prefix="/chat")

    # Initialize SocketIO with the app
    socketio.init_app(app)

    init_socketio(socketio)

    return app
