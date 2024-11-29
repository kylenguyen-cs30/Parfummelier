from app import db

product_accord = db.Table(
    "product_accord",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("accord_id", db.Integer, db.ForeignKey("accord.id")),
)


# Product model: Represents individual fragrance products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    imageURL = db.Column(db.String(200))
    description = db.Column(db.String, nullable=False)

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
    content = db.Column(db.String(500), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))


# Accord model: Represents a category of notes (e.g., Woody, Floral)
class Accord(db.Model):
    __tablename__ = "accord"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    background_color = db.Column(db.String(10))
