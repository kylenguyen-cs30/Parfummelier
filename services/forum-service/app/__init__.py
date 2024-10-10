from flask import Flask
from mongoengine import connect
from .routes import forum_blueprint

def create_app():
    app = Flask(__name__)

    # Connect to MongoDB
    connect(db="forum_service", host="localhost", port=27017)

    #register forum routes
    app.register_blueprint(forum_blueprint, url_prefix='/forum')

    return app
