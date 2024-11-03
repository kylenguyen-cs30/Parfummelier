from flask import Blueprint, request, jsonify
from app.models import db, Product, Note, Accord, Review

product_blueprint = Blueprint("product", __name__)


@product_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Product Service launched"}), 200


# ----------------------------- #
#           PRODUCTS            #
# ----------------------------- #


# NOTE: List all products with their associated notes, accord, season and review
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
                "reviews": [
                    {"rating": review.rating, "content": review.content}
                    for review in product.review
                ],
            }
            for product in products
        ]
    )


# NOTE: Retrieve a product by ID
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
            "reviews": [
                {"rating": review.rating, "content": review.content}
                for review in product.reviews
            ],
        }
    )


# NOTE: Add a new product
@product_blueprint.route("/add_product", methods=["POST"])
def add_product():
    try:
        data = request.json
        # Create a new product
        new_product = Product(
            name=data["name"],
            # designer=data.get("designer"),
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

        db.session.add(new_product)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_product.id,
                    "name": new_product.name,
                    # "designer": new_product.designer,
                    "notes": [note.name for note in new_product.notes],
                    "accords": [accord.name for accord in new_product.accords],
                },
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------------------------------------------------#
# NOTE: Update a product [Not sure yet]
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


# ----------------------------------------------------------------------------#


# NOTE: Add Review
# TODO: add token_required to attach user
@product_blueprint.route("/add_review/<int:product_id>", methods=["POST"])
def add_review(product_id):
    try:
        data = request.json

        # Find the product ID
        product = Product.query.get_or_404(product_id)

        # Create a new review
        new_review = Review(
            rating=data["rating"], content=data.get("content"), product_id=product.id
        )

        # Add the review to the product's review relationship
        db.session.add(new_review)
        db.session.commit()

        return jsonify(
            {
                "review_id": new_review.id,
                "product_id": new_review.product_id,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# NOTE: Delete a product [this part shoud be blocked]
@product_blueprint.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})


# ----------------------------- #
#          COLLECTIONS          #
# ----------------------------- #


# NOTE: List all collections
@product_blueprint.route("/collections", methods=["GET"])
def get_all_collections():
    try:
        collections = Collection.query.all()

        # Format collections data for response
        collection_list = [
            {"id": collection.id, "name": collection.name} for collection in collections
        ]

        return jsonify(collection_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# NOTE: Create a new collection
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
