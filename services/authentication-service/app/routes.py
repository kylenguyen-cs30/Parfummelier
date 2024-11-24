from types import MethodType
from flask import Blueprint, request, jsonify, url_for, current_app, make_response
from .models import User

# from flask_login import login_user, logout_user, current_user, login_required
from app import db
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timezone

import jwt
import datetime
import random
import smtplib
import os
import logging

# for logging error
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Blueprint
auth_blueprint = Blueprint("auth", __name__)

# NOTE: serializer for generating and verifying tokens
# this serializer verify and add security layer for
# JSON Authentication Token
serializer = URLSafeTimedSerializer("SECRET_KEY")


# NOTE: Home route
@auth_blueprint.route("/", methods=["get"])
def home():
    return jsonify({"message": "authentication service launched"})


# NOTE:  Login Route
@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        # Log incoming request
        logger.debug("Login attempt received")
        data = request.json
        logger.debug(f"Request data: {data}")

        # Validate input data
        if not data or "email" not in data or "password" not in data:
            logger.error("Missing required fields in request")
            return jsonify({"error": "Email and password are required"}), 400

        email = data.get("email")
        password = data.get("password")

        # Log email (but never log passwords!)
        logger.debug(f"Attempting login for email: {email}")

        # Fetch user from database
        user = User.query.filter_by(email=email).first()
        logger.debug(f"User found: {user is not None}")

        if not user:
            logger.warning(f"No user found for email: {email}")
            return jsonify({"error": "Invalid email or password"}), 401

        # Check password
        logger.debug("Checking password...")
        password_valid = user.check_password(password)
        logger.debug(f"Password valid: {password_valid}")

        if not password_valid:
            logger.warning("Invalid password attempt")
            return jsonify({"error": "Invalid email or password"}), 401

        # Generate tokens
        logger.debug("Generating tokens...")
        try:
            access_token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": datetime.datetime.now() + datetime.timedelta(hours=8),
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )

            refresh_token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": datetime.datetime.now() + datetime.timedelta(days=7),
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            logger.debug("Tokens generated successfully")

        except Exception as e:
            logger.error(f"Token generation failed: {str(e)}")
            return jsonify({"error": "Failed to generate tokens"}), 500

        # Create response
        try:
            response = make_response(
                jsonify(
                    {
                        "message": "Login successful",
                        "access_token": access_token,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                        },
                    }
                )
            )

            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                # secure=True,  # Enable in production with HTTPS
                samesite="Lax",
                path="/refresh",
                max_age=7 * 24 * 60 * 60,  # 7 days in seconds
            )
            logger.debug("Response created successfully")
            return response

        except Exception as e:
            logger.error(f"Response creation failed: {str(e)}")
            return jsonify({"error": "Failed to create response"}), 500

    except Exception as e:
        logger.error(f"Login failed with error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# NOTE: refresh access_token route:
@auth_blueprint.route("/refresh", methods=["POST"])
def refresh():
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
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),
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


# NOTE: generate short live token
def generate_password_reset_token(user_id):
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=10),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return token


# NOTE: generate code for 2fa
def generate_2fa_code():
    return str(random.randint(100000, 999999))


# NOTE: map to map the code to the email
codes = {}


# NOTE:  send verification code to email for verificaiton:
def send_email(to_email, code):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")

    print(f"Connecting to SMTP Server: {smtp_server}")

    try:
        # NOTE: Use email service to email the code
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(email_user, email_pass)
        # NOTE: Content of message
        subject = "Parfummelier Verfication Code"
        message = f"Subject: {subject} \n\n Your Verfication Code : {code}"
        server.sendmail(email_user, to_email, message)
        server.quit()

    except Exception as e:
        print(f"Failed to send email : {str(e)}")


# NOTE: Verify Code Route


@auth_blueprint.route("/verify-code", methods=["POST", "OPTIONS"])
def verify_code():
    if request.method == "OPTIONS":
        return "", 200

    email = request.json.get("email")
    entered_code = request.json.get("code")

    # No Code Exit
    if email not in codes:
        return jsonify({"Error": "No Verification Code"}), 400

    store_code_info = codes[email]
    # No more time 🕧
    if datetime.datetime.now() > store_code_info["expires"]:
        return jsonify({"Error": "Time Has expired"}), 400

    # Invalid Code ❌
    if entered_code != store_code_info["code"]:
        return jsonify({"Error": "Invalid Code"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    reset_token = generate_password_reset_token(user.id)

    del codes[email]

    return (
        jsonify(
            {
                "message": "2-F-A verified. user can change the password now ",
                "reset_token": reset_token,
            },
        ),
        200,
    )


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
@auth_blueprint.route("/forget-password", methods=["POST", "OPTIONS"])
def forget_password():
    if request.method == "OPTIONS":
        return "", 200

    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        code = generate_2fa_code()
        print(f"code is {code}")
        exp_time = datetime.datetime.now() + datetime.timedelta(minutes=4)
        codes[email] = {"code": code, "expires": exp_time}
        send_email(email, code)

        # TODO: we send user's email a 6 digit code to confirm
        return (
            jsonify(
                {
                    "message": "6 digits code send to user's email. Pop up 2-F-A verification"
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Email not found"}), 404


@auth_blueprint.route("/change-password", methods=["POST"])
def change_password():
    try:
        data = request.json
        reset_token = data.get("reset_token")  # Token provided by client
        new_password = data.get("new_password")

        if not reset_token or not new_password:
            return jsonify({"error": "reset_token and new_password are required"}), 400

        # Verify the token
        try:
            decoded_token = jwt.decode(
                reset_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user_id = decoded_token["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Reset token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid reset token"}), 401

        # Query the user by user_id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Hash the new password and update the user's password
        hashed_password = generate_password_hash(new_password)
        user.password_hash = hashed_password

        # Commit the change to the database
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        print(f"Error changing password: {e}")
        return jsonify({"error": "An error occurred while changing the password"}), 500


@auth_blueprint.route("/validate-token", methods=["POST"])
def validate_token():
    access_token = request.json.get("access_token")
    if not access_token:
        return jsonify({"error": "Access token is missing"}), 400

    try:
        decoded = jwt.decode(
            access_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )

        # check if the toke has expired
        exp = decoded.get("exp")
        # if datetime.fromtimestamp(exp) < datetime.now():
        if datetime.datetime.now(tz=timezone.utc).timestamp() > exp:
            return jsonify({"status": "expired"}), 401
        return jsonify({"status": "valid"})
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "invalid token"}), 401
