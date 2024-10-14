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
    try:
        data = request.json
        # Retrieve collectoin if provided
        collection_id = data.get("collection_id")
        collection = Collection.query.get(collection_id) if collection_id else None

        # Create a new product
        new_product = Product(
            name=data["name"],
            manufacturer=data["manufacturer"],
            designer=data.get("designer"),
            collection=collection,
        )

        # Handle Notes
        note_objects = []
        for note_name in data.get("note", []):
            note_obj = Note.query.filter_by(name=note_name).first()
            if not note_obj:
                note_obj = Note(name=note_name)
                db.session.add(note_obj)
            note_objects.append(note_obj)
        new_product.notes = note_objects

        # Handle Accords
        accord_objects = []
        for accord_name in data.get("accords", []):
            accord_obj = Accord.query.filter_by(name=accord_name).first()
            if not accord_obj:
                accord_obj = Accord(name=accord_name)
                db.session.add(accord_obj)
            accord_objects.append(accord_obj)
        new_product.accords = accord_objects

        # Handle Seasons
        season_objects = []
        for season_name in data.get("seasons", []):
            season_obj = Season.query.filter_by(name=season_name).first()
            if not season_obj:
                season_obj = Season(name=season_name)
                db.session.add(season_obj)
            season_objects.append(season_obj)
        new_product.seasons = season_objects

        db.session.add(new_product)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_product.id,
                    "name": new_product.name,
                    "manufacturer": new_product.manufacturer,
                    "designer": new_product.designer,
                    "collection": new_product.collection,
                    "notes": [note.name for note in new_product.notes],
                    "accords": [accord.name for accord in new_product.accords],
                    "seasons": [season.name for season in new_product.seasons],
                },
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


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


# ----------------------------- #
#          COLLECTIONS          #
# ----------------------------- #
