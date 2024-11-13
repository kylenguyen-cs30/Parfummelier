from app.extensions import db


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

scentBank_collections = db.Table(
    "scentBank_collections",
    db.Column("scentBank_id", db.Integer, db.ForeignKey("scent_bank.id")),
    db.Column("collection_id", db.Integer, db.ForeignKey("collection.id")),
)
