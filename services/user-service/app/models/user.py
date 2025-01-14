from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    """User model for authentication and profile information"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    # this scent id for tracking user scent bank data
    scentID = db.Column(
        db.Integer,
        db.ForeignKey("scent_bank.id"),
        nullable=True,
        unique=True,
    )

    # setting many to many relationship for each user that establish many to many relationship
    scent = db.relationship("ScentBank", backref="users", lazy=True)

    def __init__(self, userName, email, firstName, lastName, dateOfBirth, password):
        self.userName = userName
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.userName}>"
