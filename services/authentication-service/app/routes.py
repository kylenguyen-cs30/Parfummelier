from flask import Blueprint, request, jsonify, url_for
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer


auth_blueprint = Blueprint("auth", __name__)

# serializer for generating and verifying tokens
serializer = URLSafeTimedSerializer("SECRET_KEY")


# NOTE: Home route
@auth_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Authentication service launched !!!"})


# TODO: Need Test
# NOTE: Login Route
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Fetch user from the database
    user = User.query.filter_by(email=email).first()

    # check user
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in successfully !"}), 200
    else:
        return jsonify({"error": "Invalid Email"}), 401


# TODO: Need Test
# NOTE: Logout Route
@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


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
@login_required
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
