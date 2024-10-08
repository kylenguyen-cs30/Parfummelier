from app import db
from enum import unique

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# NOTE: User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    scentID = db.Column(
        db.Integer,
        db.ForeignKey("scent_bank.id"),
        nullable=True,
        unique=True,
    )  # ForeignKey to ScentBank table
    email = db.Column(db.String(100), unique=True, nullable=False)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)

    # accesss the key directly
    scent = db.relationship("ScentBank", backref="users", lazy=True)

    def __init__(self, userName, email, firstName, lastName, dateOfBirth, password):
        self.userName = userName
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.set_password(password)

    # Set password_hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.userName} created>"


# NOTE: Association Tables for many-to-many relationship

scentBank_notes = db.Table(
    "scentBank_notes",
    db.Column("scentBank_id", db.Integer, db.ForeignKey("scent_bank.id")),
    db.Column("note_id", db.Integer, db.ForeignKey("note.id")),
)

scentBank_accords = db.Table(
    "scentBank_accords",
    db.Column("scentBank_id", db.Integer, db.ForeignKey("scent_bank.id")),
    db.Column("accord_id", db.Integer, db.ForeignKey("accord.id")),
)

scentBank_products = db.Table(
    "scentBank_products",
    db.Column("scentBank_id", db.Integer, db.ForeignKey("scent_bank.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)

scentBank_seasons = db.Table(
    "scentBank_seasons",
    db.Column("scentBank_id", db.Integer, db.ForeignKey("scent_bank.id")),
    db.Column("season_id", db.Integer, db.ForeignKey("season.id")),
)

scentBank_collections = db.Table(
    "scentBank_collections",
    db.Column("scentBank_id", db.Integer, db.ForeignKey("scent_bank.id")),
    db.Column("collection_id", db.Integer, db.ForeignKey("season.id")),
)


class ScentBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_notes = db.relationship(
        "Note",
        secondary=scentBank_notes,
        backref=db.backref("scentBanks", lazy="dynamic"),
    )
    favorite_accords = db.relationship(
        "Accord",
        secondary=scentBank_accords,
        backref=db.backref("scentBanks", lazy="dynamic"),
    )
    favorite_products = db.relationship(
        "Product",
        secondary=scentBank_products,
        backref=db.backref("scentBanks", lazy="dynamic"),
    )
    favorite_seasons = db.relationship(
        "Season",
        secondary=scentBank_seasons,
        backref=db.backref("scentBanks", lazy="dynamic"),
    )
    favorite_collections = db.relationship(
        "Collection",
        secondary=scentBank_collections,
        backref=db.backref("scentBanks", lazy="dynamic"),
    )

    def __repr__(self):
        return f"ScentBank {self.id}"


# NOTE: Note Table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)


# NOTE: Accords Table
class Accord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)


# NOTE: Product Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)


# NOTE: Season Table
class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)


# NOTE: Collection Table
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=True)
