import jwt
import logging

from flask_migrate import current
from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from functools import wraps
from .models import (
    ScentBank,
    User,
    Note,
    Accord,
    Product,
)
from app import db

user_blueprint = Blueprint("user", __name__)


logger = logging.getLogger(__name__)

# TODO:
#
# ------------------------------------------------------------------------------------------#
# Token Required for JWT request
# Service to  service user need to go through JWT Checking point
#
# ------------------------------------------------------------------------------------------#

# NOTE:
# Database reset is neccessary if the token authentication are not accepted or invalid
# make sure writing the documentaion if there are unprecedented case. This service is
# reponsible for creating user account, return user's json information for client side


# NOTE: Home route
@user_blueprint.route("/")
def home():
    return jsonify("user-service launched!!")


# NOTE: Token Check point
def token_required(f):
    @wraps(f)
    def decorated(*arg, **kwargs):
        token = None

        if "Authorization" in request.headers:
            # Split Bearer <Token> into array
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            print("Token Missing")
            return jsonify({"error": "Token missing"}), 401

        try:
            print(f"Token   : {token}")
            print(f"SECRET_KEY  : {current_app.config['SECRET_KEY']}")

            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            print(f"Decoded: {data}")
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return jsonify({"error": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token is expried"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid Token"}), 401

        # Pass to the current_user to the wrapped function
        return f(current_user, *arg, **kwargs)

    return decorated


# @cross_origin(
#     origins="http://localhost:3000", headers=["Content-Type", "Authorization"]
# )


# NOTE: Add new user route
@user_blueprint.route("/register", methods=["POST", "OPTIONS"])
@cross_origin(origins="*", headers=["Content-Type", "Authorization"])
def register_user():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()

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

        # Create an empty ScentBank for this user
        new_scent_bank = ScentBank()
        db.session.add(new_scent_bank)
        db.session.commit()

        # assign the scentbank  id to the user's scentid
        new_user.scentID = new_scent_bank.id
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "User created successfully!",
                }
            ),
            202,
        )

    except Exception as e:
        # print(f"Error registering user: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"Failed to register user: {str(e)}"}), 501


# NOTE: list all users
# WARNING: This route should be disabled
#
# ----------------------------------------------------------------#
@user_blueprint.route("/users", methods=["GET", "OPTIONS"])
@cross_origin(
    origins=["http://localhost:3000"],
    methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
)
@token_required
def list_users(current_user):  # Added current_user parameter
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

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
        return jsonify({"error": f"Error fetching users: {str(e)}"}), 501


# ----------------------------------------------------------------#

# NOTE: Update ScentBank


# WARNING: Don't uncomment this line
# @user_blueprint.route("/user/<int:user_id>/scentbank", methods=["PUT", "POST"])
@user_blueprint.route("/user/scentbank", methods=["PUT", "POST"])
@cross_origin(origin="http://localhost:3000", headers=["Content-Type", "Authorization"])
@token_required
def update_scentbank_for_user(current_user):
    try:
        # Get the user's existing ScentBank
        scent_bank = ScentBank.query.get(current_user.scentID)
        if not scent_bank:
            return jsonify({"error": "ScentBank not found for this user"}), 404

        # Collect the new data from the request (allow users to add their own custom data)
        favorite_notes = request.json.get("favorite_notes", [])
        favorite_accords = request.json.get("favorite_accords", [])
        favorite_products = request.json.get("favorite_products", [])
        favorite_collections = request.json.get("favorite_collections", [])

        note_objects = scent_bank.favorite_notes if favorite_notes else None
        accord_objects = scent_bank.favorite_accords if favorite_accords else None
        product_objects = scent_bank.favorite_products if favorite_products else None
        collection_objects = (
            scent_bank.favorite_collections if favorite_collections else None
        )

        # Add new Note into ScentBank
        if favorite_notes:
            note_objects = []
            for (
                note
            ) in favorite_notes:  # extract elements from the favorite_notes array
                note_obj = Note.query.filter_by(
                    name=note
                ).first()  # query to see whether user already have Note or not
                if not note_obj:
                    note_obj = Note(name=note)
                    db.session.add(note_obj)
            note_objects.append(note_obj)

        # Add new Accord into ScentBank
        if favorite_accords:
            accord_objects = []
            for accord in favorite_accords:
                accord_obj = Accord.query.filter_by(name=accord).first()
                if not accord_obj:
                    accord_obj = Accord(name=accord)
                    db.session.add(accord_obj)
            accord_objects.append(accord_obj)

        # Add new Product into ScentBank
        if favorite_products:
            product_objects = []
            for product in favorite_products:
                product_obj = Product.query.filter_by(name=product).first()
                if not product_obj:
                    product_obj = Product(name=product)
                    db.session.add(product_obj)
            product_objects.append(product_obj)

        # Add new Collection into ScentBank
        if favorite_collections:
            collection_objects = []
            for collection in favorite_collections:
                collection_obj = Collection.query.filter_by(name=collection).first()
                if not collection_obj:
                    collection_obj = Collection(name=collection)
                    db.session.add(collection_obj)
            collection_objects.append(collection_obj)

        # Commit the new objects to the database
        db.session.commit()

        # Update the User's ScentBank with their custom data
        if note_objects:
            scent_bank.favorite_notes = note_objects
        if accord_objects:
            scent_bank.favorite_accords = accord_objects
        if product_objects:
            scent_bank.favorite_products = product_objects
        if collection_objects:
            scent_bank.favorite_collections = collection_objects

        db.session.commit()

        return jsonify({"message": "ScentBank updated successfully"}), 201

    except Exception as e:
        print(f"Error Updating ScentBank: {e}")
        db.session.rollback()
        return jsonify({"error": f"Fail to update ScentBank: {str(e)}"}), 500


# NOTE: reset db route
@user_blueprint.route("/reset-db", methods=["POST"])
def reset_db():
    try:
        # Drop all tables
        db.drop_all()

        # Recreate the tables
        db.create_all()

        # Apply migrations
        from flask_migrate import upgrade

        upgrade()

        db.session.commit()
        return jsonify({"message": "Database reset successful"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to reset database: {str(e)}"}), 500


# ------------------------------------------------------------------------------------------------#
# NOTE: Test PUT API
@user_blueprint.route("/test-put", methods=["PUT"])
# @token_required
def test_put(current_user):
    try:
        return (
            jsonify(
                {"message": "PUT is successfully tested", "user": current_user.email}
            ),
            200,
        )
    except Exception as e:
        print(f"Error : {e}")
        return jsonify({"error": f"Fail to test the PUT METHOD: {str(e)}"}), 500


# ------------------------------------------------------------------------------------------------#


# NOTE:  scent bank detail decorator
def scentbank_details(f):
    @wraps(f)
    @token_required
    def decorated_function(current_user, *arg, **kwargs):
        # find the user's scentbank
        scent_bank = ScentBank.query.get(current_user.scentID)
        if not scent_bank:
            return jsonify({"error": "scent bank not found"}), 404
        scent_bank_details = {
            "user_id": current_user.id,
            "scent_id": scent_bank.id,
            "firstName": current_user.firstName,
            "lastName": current_user.lastName,
            "email": current_user.email,
            "favorite_notes": [note.name for note in scent_bank.favorite_notes],
            "favorite_accords": [accord.name for accord in scent_bank.favorite_accords],
            "favorite_products": [
                product.name for product in scent_bank.favorite_products
            ],
            "favorite_collections": [
                collection.name for collection in scent_bank.favorite_collections
            ],
        }
        return f(scent_bank_details, *arg, **kwargs)

    return decorated_function


@user_blueprint.route("/user/scentbank/details", methods=["GET"])
@cross_origin(origin="http://localhost:3000", headers=["Content-Type", "Authorization"])
@scentbank_details
# def get_user_scentbank_details(scent_bank_details, user_id):
def get_user_scentbank_details(scent_bank_details):
    return jsonify(scent_bank_details), 200


# WARNING: This route should be disabled for security reason.
# let me know if you need to open this route


# NOTE: Return all basic informations based on one user
@user_blueprint.route("/user", methods=["GET"])
@token_required
def get_user_details(current_user):
    try:
        user_details = {
            "firstName": current_user.firstName,
            "lastName": current_user.lastName,
            "email": current_user.email,
            "dateOfBirth": current_user.dateOfBirth.strftime("%Y-%m-%d"),
        }
        return jsonify(user_details), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching users: {str(e)}"}), 501


"""
This route will return user's information when a chat is initialized
"""


@user_blueprint.route("/user/chat-info", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
@token_required
def get_user_chat_info(current_user):
    """
    Get minimal user information needed for chat features.
    """
    try:
        user_details = {
            "firstName": current_user.firstName,
            "lastName": current_user.lastName,
            "userName": current_user.userName,
            "userId": current_user.id,
        }

        return jsonify(user_details), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching users: {str(e)}"}), 501


@user_blueprint.route("/user/<int:user_id>/chat-info", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
@token_required
def get_user_chat_info_by_id(current_user, user_id):
    """
    Get minimal user information needed for chat features by user ID.
    Requires authentication to prevent unauthorized access to user information.
    """
    try:
        # Optionally, you could add additional checks here
        # For example, verify if current_user has permission to view this info

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_details = {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "userName": user.userName,
            "userId": user.id,
        }

        return jsonify(user_details), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching user: {str(e)}"}), 501


# NOTE: Return user information
@user_blueprint.route("/current-user/info", methods=["GET"])
@token_required
def get_user_info(current_user):
    try:
        user_info = {
            "id": current_user.id,
            "email": current_user.email,
            "firstName": current_user.firstName,
            "lastName": current_user.lastName,
            "userName": current_user.userName,
        }

        return jsonify(user_info), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching user info: {str(e)}"}), 500


# NOTE: Return Favorite Collections

# NOTE: Delete a user
# @user_blueprint.route("/user/<int:user_id>/delete", methods=["DELETE"])
# def delete_user(user_id):
#     try:
#         user = User.query.get(user_id)
#         if not user:
#             return jsonify({"error": "User not Found"}), 404
#
#         # Delete the user from the database
#         db.session.delete(user)
#         db.session.commit()
#         return (
#             jsonify(
#                 {
#                     "message": f"User {user.firstName} {user.lastName} delete successfully"
#                 }
#             ),
#             200,
#         )
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": f"Failed to delete user : {str(e)}"}), 500
#
