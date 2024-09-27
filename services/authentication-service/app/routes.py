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

            # NOTE: Return as JSON
            #
            # return (
            #     jsonify(
            #         {
            #             "message": "Login successfully",
            #             "access_token": access_token,
            #             "refresh_token": refresh_token,
            #         }
            #     ),
            #     200,
            # )

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

        ##########################################################################
        # return (
        #     jsonify({"access_token": access_token, "refresh_token": refresh_token}),
        #     200,
        # )
        ##########################################################################

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


# NOTE: Forget password before Login
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


# NOTE: Change password after login
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


# NOTE: Change Password before login (After clicking Reset Password Link)
@auth_blueprint.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        # generate a secure token
        token = serializer.dumps(user.email, salt="password-reset-salt")

        # build a reset url
        reset_url = url_for("auth.reset_password", token=token, _external=True)

        # TODO:
        # adding SMTP Server to send an email link to user's email

        return jsonify({"message": "email sent successfully"}), 200
    else:
        return jsonify({"error": "Email not Found"}), 404


# NOTE: Reset Password (Changing the password using the token)
@auth_blueprint.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    try:
        # Verify the token with a max age of 1 hour (3600 seconds)
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)
    except Exception as e:
        return jsonify({"error": "The reset link is invalid or expired"}), 400

    # Fetch the user by email
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get the new password from the request
    new_password = request.json.get("new_password")

    # Update the user's password
    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200
