from app import db


# NOTE: Accociation table for many-to-many relationship

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


# PERF: Product model: Represents individual fragrance products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designer = db.Column(db.String(100), nullable=False)

    # One-To-Many relationship
    # collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))

    # many-to-many relationship
    notes = db.relationship(
        "Note", secondary=product_note, backref=db.backref("products", lazy="dynamic")
    )
    accords = db.relationship(
        "Accord",
        secondary=product_accord,
        backref=db.backref("products", lazy="dynamic"),
    )

    review = db.relationship("Review", backref="product", lazy="dynamic")


# PERF: Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))


# PERF: Accord model: Represents a category of notes (e.g., Woody, Floral)
class Accord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


# PERF: Note model: Represents a fragrance note belonging to a specific accord
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
