from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture = db.Column(db.String(100), nullable=False)
    top_notes = db.Column(db.String(100))
