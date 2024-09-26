from app import db


# TODO: Create a table for Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture = db.Column(db.String(100), nullable=False)


top_notes = db.Column(db.String(100))


# TODO: Create a Table for Collection Many-To-One Relationships
