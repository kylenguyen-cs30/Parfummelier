from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from .routes import forum_blueprint
import os

# Initialize SocketIO
socketio = SocketIO()

def create_app():
    # Specify the static folder where your frontend files are located
    app = Flask(__name__, static_folder='../frontend/app/chat-page')

    # Register routes for the forum
    app.register_blueprint(forum_blueprint)

    # Initialize SocketIO with the app
    socketio.init_app(app)

    # Route to serve the chat.html page
    @app.route('/chat')
    def serve_chat():
        return send_from_directory(app.static_folder, 'chat.html')

    return app
