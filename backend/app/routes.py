import logging
import os
from .models import User
from . import db
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request, send_from_directory

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return jsonify(
        {"message": "Welcome to My Pet Shop!"}
    )  # Improved message consistency
