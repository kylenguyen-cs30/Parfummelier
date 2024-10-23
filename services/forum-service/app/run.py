# Will be used to test Flask with Flask-SocketIO

from app import create_app, socketio  # Import socketio from __init__.py

app = create_app()

if __name__ == "__main__":
    # Use socketio.run() instead of app.run() to support WebSocket functionality
    socketio.run(app, debug=True)
