from app import db


# Accord model: Represents a category of notes (e.g., Woody, Floral)
class Accord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


# Note model: Represents a fragrance note belonging to a specific accord
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    accord_id = db.Column(db.Integer, db.ForeignKey("accord.id"), nullable=False)

    # Relationship to link a note to its accord
    accord = db.relationship("Accord", backref="notes")


# Association table to manage the Many-to-Many relationship between Product and Note
product_notes = db.Table(
    "product_notes",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
)


# Collection model: Represents a collection of products (e.g., Bleu de Chanel)
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    designer = db.Column(db.String(100), nullable=False)


# Product model: Represents individual fragrance products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designer = db.Column(db.String(100), nullable=False)
    year_released = db.Column(db.Integer, nullable=True)
    season = db.Column(
        db.String(50), nullable=True
    )  # Represents the season associated with the product
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=True)

    # Relationship to associate multiple notes with a product
    notes = db.relationship("Note", secondary=product_notes, backref="products")

    # Connect the product with the Collection
    collection = db.relationship("Collection", backref="products")
