import string
import os

# import smtplib [optional]
from flask import Blueprint, request, jsonify
from .models import ScentBank, User, Note, Scent, Accord, Season
from app import db

user_blueprint = Blueprint("user", __name__)


# NOTE: Add new user route
@user_blueprint.route("/register", methods=["POST"])
def register_user():
    try:
        #############################################################
        # firstName = request.form.get("firstName")
        # lastName = request.form.get("lastName")
        # email = request.form.get("email")
        # password = request.form.get("password")
        # userName = request.form.get("userName")
        # dateOfBirth = request.form.get("dob")
        #############################################################
        firstName = request.json.get("firstName")
        lastName = request.json.get("lastName")
        email = request.json.get("email")
        password = request.json.get("password")
        userName = request.json.get("userName")
        dateOfBirth = request.json.get("dob")

        # checking if the user already
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this email already existed"}), 401

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

        # Create a new ScentBank for this user
        new_scent_bank = ScentBank(
            favorite_notes=[],
            favorite_accords=[],
            favorite_scents=[],
            favorite_seasons=[],
        )

        db.session.add(new_scent_bank)
        db.session.commit()

        # Assign the ScentBank Id to the user's scentID
        new_user.scentID = new_scent_bank.id
        db.session.commit()

        #############################################################
        # Generate scentID base on user's name and user_id
        # first_initial_ascii = ord(firstName[1].upper())
        # last_initial_ascii = ord(lastName[1].upper())
        # scentID = int(f"{first_initial_ascii}{last_initial_ascii}{new_user.id}")
        # print(scentID)

        # Update scentID
        # new_user.scentID = scentID
        # db.session.commit()
        #############################################################

        return (
            jsonify(
                {
                    "message": "User created successfully!",
                    "user_id": new_user.id,
                    "scentID": new_scent_bank.id,
                }
            ),
            202,
        )

    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({"error": f"Failed to register user : {str(e)}"}), 501


# NOTE: Home route
@user_blueprint.route("/")
def home():
    return jsonify("user-service launched!!")


# NOTE: list all users
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


# NOTE: list a ScentBank associated specificed user
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


# NOTE: Update ScentBank Details for User
@user_blueprint.route("/user/<int:user_id>/scentbank", methods=["PUT", "POST"])
def add_scentbank_for_user(user_id):
    try:
        # find user by user_id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User is not found"}), 404

        # Get the user's existing ScentBank
        scent_bank = ScentBank.query.get(user.scentID)
        if not scent_bank:
            return jsonify({"error": "ScentBank not found for this user"}), 404
        # Collect data
        favorite_notes = request.json.get("favorite_notes", [])
        favorite_accords = request.json.get("favorite_accords", [])
        favorite_scents = request.json.get("favorite_scents", [])
        favorite_seasons = request.json.get("favorite_seasons", [])

        # Validate and retrieve the corresponding objects from the database
        note_objects = Note.query.filter(Note.name.in_(favorite_notes)).all()
        accord_objects = Accord.query.filter(Accord.name.in_(favorite_accords)).all()
        scent_objects = Scent.query.filter(Scent.name.in_(favorite_scents)).all()
        season_objects = Season.query.filter(Season.name.in_(favorite_seasons)).all()

        # Update the User's ScentBank with the new database
        scent_bank.favorite_notes = note_objects
        scent_bank.favorite_accords = accord_objects
        scent_bank.favorite_scents = scent_objects
        scent_bank.favorite_seasons = season_objects

        #############################################################

        # create new scent bank  bank entry for the user
        # new_scent_bank = ScentBank(
        #     favorite_notes=note_objects,
        #     favorite_accords=accord_objects,
        #     favorite_scents=scent_objects,
        #     favorite_seasons=season_objects,
        # )
        #
        # Assign the scent bank to the user
        # user.scent = new_scent_bank

        # Assign the scent bank id
        # user.scentID = new_scent_bank.id

        # Add and Commit
        # db.session.add(new_scent_bank)
        #
        #############################################################

        db.session.commit()

        return jsonify({"message": "Scent Bank added successfully"}), 201

    except Exception as e:
        print(f"Error adding ScentBank: {e}")
        return jsonify({"error": f"Failed to add ScentBank : {str(e)}"}), 500


# NOTE: Test PUT methods
@user_blueprint.route("/test-put", methods=["PUT"])
def test_put():
    return jsonify({"message": "PUT Method works"}), 200
