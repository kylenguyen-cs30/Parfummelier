from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from app.chat import chat_blueprint, register_socketio_events

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register the chat blueprint
    app.register_blueprint(chat_blueprint, url_prefix="/chat")

    # Initialize SocketIO
    socketio.init_app(app)

    # Register the WebSocket events after socketio initialization
    register_socketio_events(socketio)

    return app
