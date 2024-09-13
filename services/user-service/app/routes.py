import string
import os

# import smtplib [optional]
from flask import Blueprint, request, jsonify
from .models import User
from app import db

user_blueprint = Blueprint("user", __name__)


# NOTE: Add new user route
@user_blueprint.route("/register", methods=["POST"])
def register_user():
    try:
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        userName = request.form.get("userName")
        dateOfBirth = request.form.get("dob")

        # checking if the user already
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this email already existed"}), 400

        # create a new user
        new_user = User(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
            dateOfBirth=dateOfBirth,
            userName=userName,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201

    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({"error": f"Failed to register user : {str(e)}"}), 500


# Home route
@user_blueprint.route("/")
def home():
    return jsonify("user-service launched!!")


# list all users
@user_blueprint.route("/users", methods=["GET"])
def list_users():
    try:
        users = User.query.all()
        user_list = [
            {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "dateOfBirth": user.dateOfBirth.strftime("%Y-%m-%d"),
                "scentID": user.scentID,
            }
            for user in users
        ]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching users: {str(e)}"}), 500


# list all user with ScentBank
