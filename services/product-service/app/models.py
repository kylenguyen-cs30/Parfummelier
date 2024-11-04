from app import db

# Collection model
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
# Association tables for many-to-many relationships
product_note = db.Table(
    "product_note",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("note_id", db.Integer, db.ForeignKey("note.id")),
)

product_accord = db.Table(
    "product_accord",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("accord_id", db.Integer, db.ForeignKey("accord.id")),
)

# Product model: Represents individual fragrance products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)  # Changed from designer to manufacturer
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=True)
    collection = db.relationship('Collection', backref=db.backref('products', lazy=True))

    # Many-to-many relationships
    notes = db.relationship(
        "Note", secondary=product_note, backref=db.backref("products", lazy="dynamic")
    )
    accords = db.relationship(
        "Accord",
        secondary=product_accord,
        backref=db.backref("products", lazy="dynamic"),
    )

    # One-to-many relationship with reviews
    reviews = db.relationship("Review", backref="product", lazy="dynamic")

# Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

# Accord model: Represents a category of notes (e.g., Woody, Floral)
class Accord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# Note model: Represents a fragrance note belonging to a specific accord
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
