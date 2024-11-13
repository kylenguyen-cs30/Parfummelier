from app.extensions import db
from .associations import (
    scentBank_accords,
    scentBank_products,
    scentBank_collections,
)


class ScentBank(db.Model):
    """ScentBank model for storing user's scent preferences"""

    __tablename__ = "scent_bank"

    id = db.Column(db.Integer, primary_key=True)

    # Relationships

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
    favorite_collections = db.relationship(
        "Collection",
        secondary=scentBank_collections,
        backref=db.backref("scentBanks", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<ScentBank {self.id}>"


class Accord(db.Model):
    __tablename__ = "accord"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Collection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
