from types import MethodType
from flask import Blueprint, request, jsonify, url_for, current_app, make_response
from .models import User

# from flask_login import login_user, logout_user, current_user, login_required
from app import db
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
import jwt
import datetime


auth_blueprint = Blueprint("auth", __name__)

# NOTE: serializer for generating and verifying tokens
# this serializer verify and add security layer for
# JSON Authentication Token
serializer = URLSafeTimedSerializer("SECRET_KEY")


# NOTE: Home route
@auth_blueprint.route("/", methods=["get"])
def home():
    return jsonify({"message": "authentication service launched !!!"})


# NOTE: New Login Route
@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # fetch user user from database
        user = User.query.filter_by(email=email).first()

        # check user
        if user and user.check_password(password):
            # NOTE: generate access token
            access_token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )

            # NOTE: generate JWT
            refresh_token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": datetime.datetime.now() + datetime.timedelta(days=7),
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )

            # set response HTTP Cookie only
            response = make_response(
                jsonify({"message": "Login successfully", "access_token": access_token})
            )

            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                # secure=True,
                samesite="Lax",
                path="/refresh",
            )
            return response

        else:
            return jsonify({"error": "invalid email"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Unknown error"}), 500


# NOTE: refresh access_token route:
@auth_blueprint.route("/refresh", methods=["POST"])
def refresh():
    # token = request.json.get("refresh_token")
    # old_refresh_token = request.json.get("refresh_token") NOTE: we don't need this

    try:
        old_refresh_token = request.cookies.get("refresh_token")

        if not old_refresh_token:
            return jsonify({"error": "Refresh Token missing "}), 401

        # NOTE: decode the token
        data = jwt.decode(
            old_refresh_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )

        user_id = data["user_id"]

        # Query user
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "Invalid user"}), 404

        # NOTE: Generate new access token
        access_token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        # NOTE: Generate new refresh token
        refresh_token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.now() + datetime.timedelta(days=7),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        response = make_response(
            jsonify({"message": "refresh successfully", "access_token": access_token})
        )

        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            # secure=True,
            samesite="Lax",
            path="/refresh",
        )
        return response
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired. Please login again"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


# NOTE: Logout Route
# WARNING: No need this route anymore
#
###########################################################################
# @auth_blueprint.route("/logout", methods=["POST"])
# def logout():
#     return jsonify({"message": "Logged out successfully"}), 200
##########################################################################


# TODO:
# we need time to finallize this feature.
# - set up email service
# - set up App Password to use email service
# - set up SMTP server to create connection link
# - set up testing api endpoint and form from frontend
##########################################################################
# NOTE: Forget password intializaiton
# user send request to server check email and username to check
# if the userName and email matched. if they are matched, client change
# the website to the different page.
@auth_blueprint.route("/forget-password", methods=["POST"])
def forget_password():
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        # WARNING: We have to implement duo authentications and resetlink
        # so user can reset safely
        return jsonify({"message": "password reset link send to your email"}), 200
    else:
        return jsonify({"error": "Email not found"}), 404


# NOTE: After verifying user's information. we help user change the password
# from old password to new password. this
@auth_blueprint.route("/change-password", methods=["POST"])
def change_password():
    data = request.json
    old_pass = data.get("old_password")
    new_pass = data.get("new_password")

    if current_user.check_password(old_pass):
        # Update the password
        current_user.set_password(new_pass)
        db.session.commit()
        return jsonify({"message": "password changed successfully"}), 200
    else:
        return jsonify({"error": "old password is incorrect"}), 401
