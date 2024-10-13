from flask import Blueprint, request, jsonify
from app.models import db, Product, Collection, Note, Accord, Season, Review

product_blueprint = Blueprint("products", __name__)

# ----------------------------- #
#           PRODUCTS            #
# ----------------------------- #


# List all products with their associated notes, accord, season and review
@product_blueprint.route("/products", methods=["GET"])
def list_products():
    products = Product.query.all()
    return jsonify(
        [
            {
                "id": product.id,
                "name": product.name,
                "designer": product.designer,
                "manufacture": product.manufacture,
                "notes": [note.name for note in product.notes],
                "accords": [accord.name for accord in product.accords],
                "seasons": [season.name for season in product.seasons],
                "reviews": [
                    {"rating": review.rating, "content": review.content}
                    for review in product.review
                ],
            }
            for product in products
        ]
    )


# Retrieve a product by ID
@product_blueprint.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "designer": product.designer,
            "manufacture": product.manufacture,
            "collection": product.collection.name if product.collection else None,
            "notes": [note.name for note in product.notes],
            "accords": [accord.name for accord in product.accords],
            "seasons": [season.name for season in product.seasons],
            "reviews": [
                {"rating": review.rating, "content": review.content}
                for review in product.reviews
            ],
        }
    )


# Add a new product
@product_blueprint.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    collection_id = data.get("collection_id")
    new_product = Product(
        name=data["name"],
        designer=data.get("designer"),
        year_released=data.get("year_released"),
        collection_id=collection_id,
    )
    db.session.add(new_product)
    db.session.commit()
    return (
        jsonify(
            {
                "id": new_product.id,
                "name": new_product.name,
                "designer": new_product.designer,
                "year_released": new_product.year_released,
                "collection": (
                    new_product.collection.name if new_product.collection else None
                ),
            }
        ),
        201,
    )


# Update a product
@product_blueprint.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get("name", product.name)
    product.designer = data.get("designer", product.designer)
    product.year_released = data.get("year_released", product.year_released)
    product.collection_id = data.get("collection_id", product.collection_id)
    db.session.commit()
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "designer": product.designer,
            "year_released": product.year_released,
            "collection": product.collection.name if product.collection else None,
        }
    )


# Delete a product
@product_blueprint.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})


# ----------------------------- #
#          COLLECTIONS          #
# ----------------------------- #


# List all collections
@product_blueprint.route("/collections", methods=["GET"])
def list_collections():
    collections = Collection.query.all()
    return jsonify(
        [
            {
                "id": collection.id,
                "name": collection.name,
                "designer": collection.designer,
            }
            for collection in collections
        ]
    )


# Create a new collection
@product_blueprint.route("/collections", methods=["POST"])
def create_collection():
    data = request.json
    new_collection = Collection(name=data["name"], designer=data["designer"])
    db.session.add(new_collection)
    db.session.commit()
    return (
        jsonify(
            {
                "id": new_collection.id,
                "name": new_collection.name,
                "designer": new_collection.designer,
            }
        ),
        201,
    )


# List all products under a specific collection
@product_blueprint.route("/collections/<int:id>/products", methods=["GET"])
def list_products_under_collection(id):
    collection = Collection.query.get_or_404(id)
    return jsonify(
        [
            {
                "id": product.id,
                "name": product.name,
                "designer": product.designer,
                "year_released": product.year_released,
                "season": product.season,
                "notes": [
                    {"id": note.id, "name": note.name, "accord": note.accord.name}
                    for note in product.notes
                ],
            }
            for product in collection.products
        ]
    )


# ----------------------------- #
#           ACCORDS             #
# ----------------------------- #


# List all accords
@product_blueprint.route("/accords", methods=["GET"])
def list_accords():
    accords = Accord.query.all()
    return jsonify([{"id": accord.id, "name": accord.name} for accord in accords])


# ----------------------------- #
#            NOTES              #
# ----------------------------- #


# List all notes with their associated accord
@product_blueprint.route("/notes", methods=["GET"])
def list_notes():
    notes = Note.query.all()
    return jsonify(
        [
            {"id": note.id, "name": note.name, "accord": note.accord.name}
            for note in notes
        ]
    )
