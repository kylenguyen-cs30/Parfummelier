import string
import os
import logging

# import smtplib [optional]
from flask import Blueprint, request, jsonify
from .models import (
    ScentBank,
    User,
    Note,
    Scent,
    Accord,
    Season,
    scentBank_notes,
    scentBank_accords,
    scentBank_scents,
    scentBank_seasons,
)
from app import db

user_blueprint = Blueprint("user", __name__)
logging.basicConfig(level=logging.INFO)


# NOTE: Add new user route
@user_blueprint.route("/register", methods=["POST"])
#############################################################
def register_user():
    try:
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
        db.session.add(new_user)  # add new user to database
        db.session.commit()  # commit the adding action

        #############################################################
        # Default Values for the new user's scentbank
        # default_notes = Note.query.filter(Note.name.in_(["Citrus", "Floral"])).all()
        # default_accords = Accord.query.filter(Accord.name.in_(["Fresh", "Woody"])).all()
        # default_scents = Scent.query.filter(
        #     Scent.name.in_(["Strong", "Long-Lasting"])
        # ).all()
        # default_seasons = Season.query.filter(
        #     Season.name.in_(["Summer", "Spring"])
        # ).all()

        #############################################################
        # Create a new ScentBank for this user
        # new_scent_bank = ScentBank(
        #     favorite_notes=default_notes,
        #     favorite_accords=default_accords,
        #     favorite_scents=default_scents,
        #     favorite_seasons=default_seasons,
        # )
        #############################################################

        # Check and insert default values for notes, accords, scents, and seasons if they don't exist
        default_notes = ["Citrus", "Floral"]
        default_accords = ["Fresh", "Woody"]
        default_scents = ["Strong", "Long-Lasting"]
        default_seasons = ["Summer", "Spring"]

        # Insert notes if they don't exist
        for note_name in default_notes:
            if not Note.query.filter_by(name=note_name).first():
                new_note = Note(name=note_name)
                db.session.add(new_note)

        # Insert accords if they don't exist
        for accord_name in default_accords:
            if not Accord.query.filter_by(name=accord_name).first():
                new_accord = Accord(name=accord_name)
                db.session.add(new_accord)

        # Insert scents if they don't exist
        for scent_name in default_scents:
            if not Scent.query.filter_by(name=scent_name).first():
                new_scent = Scent(name=scent_name)
                db.session.add(new_scent)

        # Insert seasons if they don't exist
        for season_name in default_seasons:
            if not Season.query.filter_by(name=season_name).first():
                new_season = Season(name=season_name)
                db.session.add(new_season)

        # commit data insertion
        db.session.commit()

        # Now that the records exist, fetch them to associate with the user's ScentBank
        note_objects = Note.query.filter(Note.name.in_(default_notes)).all()
        accord_objects = Accord.query.filter(Accord.name.in_(default_accords)).all()
        scent_objects = Scent.query.filter(Scent.name.in_(default_scents)).all()
        season_objects = Season.query.filter(Season.name.in_(default_seasons)).all()

        # Create a new ScentBank for this user
        new_scent_bank = ScentBank(
            favorite_notes=note_objects,
            favorite_accords=accord_objects,
            favorite_scents=scent_objects,
            favorite_seasons=season_objects,
        )

        db.session.add(new_scent_bank)
        db.session.commit()

        # Assign the ScentBank Id to the user's scentID
        new_user.scentID = new_scent_bank.id
        db.session.commit()

        #############################################################
        #
        # new_scent_bank = ScentBank()
        # db.session.add(new_scent_bank)
        # db.session.commit()
        #
        # # ScentBank is created, associate the default Values
        # new_scent_bank.favorite_notes = default_notes
        # new_scent_bank.favorite_accords = default_accords
        # new_scent_bank.favorite_scents = default_scents
        # new_scent_bank.favorite_seasons = default_seasons
        #
        # # commit the changes to the scent bank
        # db.session.commit()
        #
        # # Assign the ScentBank Id to the user's scentID
        # # Do we need to do something like this in order to map the key from scentBank to Accord table
        # new_user.scentID = new_scent_bank.id
        # new_accord = Accord()
        # new_accord.id = new_user.scentID
        # new_accord.name = default_notes
        #
        #############################################################

        db.session.commit()
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

        #############################################################
        #
        # # Validate and retrieve the corresponding objects from the database
        # note_objects = Note.query.filter(Note.name.in_(favorite_notes)).all()
        # accord_objects = Accord.query.filter(Accord.name.in_(favorite_accords)).all()
        # scent_objects = Scent.query.filter(Scent.name.in_(favorite_scents)).all()
        # season_objects = Season.query.filter(Season.name.in_(favorite_seasons)).all()
        #
        #############################################################
        # Retrieve the corresponding objects from the database
        note_objects = Note.query.filter(Note.id.in_(favorite_notes)).all()
        accord_objects = Accord.query.filter(Accord.id.in_(favorite_accords)).all()
        scent_objects = Scent.query.filter(Scent.id.in_(favorite_scents)).all()
        season_objects = Season.query.filter(Season.id.in_(favorite_seasons)).all()

        logging.info(f"Note objects: {note_objects}")
        logging.info(f"Accord objects: {accord_objects}")
        logging.info(f"Scent objects: {scent_objects}")
        logging.info(f"Season objects: {season_objects}")
        # Update the User's ScentBank with the new database
        scent_bank.favorite_notes = note_objects
        scent_bank.favorite_accords = accord_objects
        scent_bank.favorite_scents = scent_objects
        scent_bank.favorite_seasons = season_objects
        db.session.commit()

        return jsonify({"message": "Scent Bank added successfully"}), 201

    except Exception as e:
        print(f"Error adding ScentBank: {e}")
        db.session.rollback()  # roll back if something happen
        return jsonify({"error": f"Failed to add ScentBank : {str(e)}"}), 500


#############################################################
## PERPLEXITY ## def register_user():
#     try:
#         firstName = request.json.get("firstName")
#         lastName = request.json.get("lastName")
#         email = request.json.get("email")
#         password = request.json.get("password")
#         userName = request.json.get("userName")
#         dateOfBirth = request.json.get("dob")
#
#         # checking if the user already exists
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             return jsonify({"error": "User with this email already exists"}), 401
#
#         # Create a new ScentBank
#         new_scent_bank = ScentBank()
#         db.session.add(new_scent_bank)
#         db.session.flush()  # This assigns an ID to new_scent_bank
#
#         # create a new user with the ScentBank
#         new_user = User(
#             firstName=firstName,
#             lastName=lastName,
#             email=email,
#             password=password,
#             dateOfBirth=dateOfBirth,
#             userName=userName,
#             scentID=new_scent_bank.id,  # Assign the ScentBank ID here
#         )
#         db.session.add(new_user)
#
#         db.session.commit()
#
#         return (
#             jsonify(
#                 {
#                     "message": "User created successfully!",
#                     "user_id": new_user.id,
#                     "scentID": new_scent_bank.id,
#                 }
#             ),
#             201,
#         )  # 201 is more appropriate for resource creation
#
#     except Exception as e:
#         db.session.rollback()  # Rollback in case of error
#         print(f"Error registering user: {e}")
#         return (
#             jsonify({"error": f"Failed to register user: {str(e)}"}),
#             500,
#         )  # 500 for server error
#
##############################################################
