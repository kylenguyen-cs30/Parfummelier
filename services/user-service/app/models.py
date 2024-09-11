from app import db
from enum import unique

# from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scentID = db.Column(
        db.Integer, db.ForeignKey("scent.id"), nullable=True, unique=True
    )  # ForeignKey to Favorites Scent table
    email = db.Column(db.String(100), unique=True, nullable=False)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)

    # accesss the key directly
    scent = db.relationship("Scent", backref="users", lazy=True)

    def __init__(self, userName, email, firstName, lastName, dateOfBirth):
        self.userName = userName
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth

    # Set password_hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.userName} created>"


class Scent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_products = db.Column(db.String(255), nullable=True)
    favorite_traits = db.Column(db.String(255), nullable=True)
    favorite_potency_level = db.Column(db.String(50), nullable=True)
    favorite_brand = db.Column(db.String(100), nullable=True)

    def __init__(
        self,
        favorite_products,
        favorite_traits,
        favorite_potency_level,
        favorite_brand,
    ):
        self.favorite_products = favorite_products
        self.favorite_traits = favorite_traits
        self.favorite_potency_level = favorite_potency_level
        self.favorite_brand = favorite_brand

    def __repr__(self):
        return f"Scent {self.favorite_brand}"
