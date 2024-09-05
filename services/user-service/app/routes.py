from flask import Blueprint, request, jsonify
from app.models import User
from app import db

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    user = User(email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201


@user_blueprint.route("/")
def home():
    return jsonify("user-service launched!!")
