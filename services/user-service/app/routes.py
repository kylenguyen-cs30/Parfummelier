import string
import os

# import smtplib [optional]
from flask import Blueprint, request, jsonify
from .models import ScentBank, User
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

        # Generate scentID base on user's name and user_id
        scentID = f"{firstName[0].upper()}{lastName[0].upper()}{new_user.id}"

        # Update scentID
        new_user.scentID = scentID
        db.session.commit()  # Commit the update to the database
        return (
            jsonify({"message": "User created successfully!", "scentID": scentID}),
            201,
        )

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


# list a ScentBank associated specificed user


@user_blueprint.route("/user/<int:user_id>/scentbank", methods=["GET"])
def get_scentbank_for_user(user_id):
    try:
        # Find user by user_id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user not found"}), 404

        # Find the associated ScentBank using user's scentID
        scent_bank = ScentBank.query.get(user.scentID)
        if not scent_bank:
            return jsonify({"error": "No ScentBank found for this user"}), 404

        # gather ScentBank Details
        scent_bank_details = {
            "id": scent_bank.id,
            "favorite_notes": [note.name for note in scent_bank.favorite_notes],
            "favorite_accords": [accord.name for accord in scent_bank.favorite_accords],
            "favorite_scents": [scent.name for scent in scent_bank.favorite_scents],
            "favorite_seasons": [season.name for season in scent_bank.favorite_seasons],
        }

        # include user detail
        user_details = {
            "username": user.userName,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
        }

        # Combine user details and scent bank details
        result = {
            "user": user_details,
            "scentBank": scent_bank_details,
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Error fetching ScentBank details: {str(e)}"}), 500
