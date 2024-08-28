from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# lass Pet(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     type = db.Column(db.String(50), nullable=False)
#     breed = db.Column(db.String(100), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     imageFilename = db.Column(db.Text, nullable=False)
#     gender = db.Column(db.String(10), nullable=False)
#
#     def __init__(
#         self, name, type, breed, age, price, description, imageFilename, gender
#     ):
#         self.name = name
#         self.type = type
#         self.breed = breed
#         self.age = age
#         self.price = price
#         self.description = description
#         self.imageFilename = imageFilename
#         self.gender = gender
#
#     def __repr__(self) -> str:
#         return f"<Pet{self.name}>"
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     email = db.Column(db.String(150), nullable=False, unique=True)
#     password_hash = db.Column(db.String(128), nullable=False)
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     def __repr__(self) -> str:
#         return f"<User {self.username}>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
