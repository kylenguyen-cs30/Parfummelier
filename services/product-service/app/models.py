from app import db


# NOTE: Collection model: Represents a collection of products (e.g., Bleu de Chanel)
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship("Product", backref="collection", lazy="dynamic")


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
product_season = db.Table(
    "product_season",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("season_id", db.Integer, db.ForeignKey("season.id")),
)


# PERF: Product model: Represents individual fragrance products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    designer = db.Column(db.String(100), nullable=False)

    # One-To-Many relationship
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    # collection = db.relationship("Collection", backref="products")

    # many-to-many relationship
    notes = db.relationship(
        "Note", secondary=product_note, backref=db.backref("products", lazy="dynamic")
    )
    accords = db.relationship(
        "Accord",
        secondary=product_accord,
        backref=db.backref("products", lazy="dynamic"),
    )
    seasons = db.relationship(
        "Season",
        secondary=product_season,
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


# PERF: Note model: Represents a fragrance note belonging to a specific accord
class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
