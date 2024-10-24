from flask import Flask, send_from_directory

from flask_socketio import SocketIO
from flask_cors import CORS
from pymongo import MongoClient
from app.socketio import socketio

# from app.forum_blueprint.routes import forum_blueprint

import os

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes after initializing app and socketio
from app.chat_route import routes

# NOTE: Set up MongoDB connection

mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017/chat_database")
client = MongoClient(mongo_uri)
db = client["chat_database"]  # This is the database name
# db.list_collection_names()


# Add error handling and connection test
try:
    # verify the connection
    client.admin.command("ismaster")
    print("MongoDB connection successful")

    # List connection
    print("available collections:", db.list_collection_names())

    # set up collection
    chatrooms_collection = db["chatrooms"]  # Chatrooms collection
    messages_collection = db["messages"]  # Messages collection

    # Optional
    # chatrooms_collection.create_index([("participants", 1)])
    # messages_collection.create_index([("chatroom_id", 1), ("timestamp", -1)])
    #
    def test_mongo_connection():
        try:
            test_doc = {"name": "test", "status": "success"}
            result = db.test_mongo_connection.insert_one(test_doc)
            print(f"Inserted Document with id {result.inserted_id}")
            retrieved = db.test_collection.find_one({"name": "test"})

            print(f"retrieved document: {retrieved}")

            db.test_collection.delete_one({"name": "test"})
            print("Test Document Deleted")

            return True
        except Exception as e:
            print(f"Failed Test: {str(e)}")
            return False

    if test_mongo_connection():
        print("MongoDB setup is ready for testing")
    else:
        print("MongoDB setup failed")

except Exception as e:
    print("MongoDB connection failed")


def create_app():
    # Specify the static folder where your frontend files are located
    app = Flask(__name__)
    CORS(
        app,
        # resources={r"/*": {"origins": "http://localhost:3000/"}},
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

    # Register the forum blueprint
    # app.register_blueprint(forum_blueprint, url_prefix="/forum")

    # Register the chat blueprint
    from app.chat_route.routes import chat_blueprint

    app.register_blueprint(chat_blueprint, url_prefix="/chat")

    # Initialize SocketIO with the app
    socketio.init_app(app)

    # init_socketio(socketio)

    return app


# Ensure MongoDB connection is closed
import atexit

atexit.register(client.close)
