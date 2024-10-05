from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    return app