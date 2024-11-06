from flask import Blueprint, request, jsonify
from app.models import db, Product, Accord, Review  

product_blueprint = Blueprint("product", __name__)

@product_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Product Service launched"}), 200

# ----------------------------- #
#           PRODUCTS            #
# ----------------------------- #

@product_blueprint.route("/products", methods=["GET"])
def list_products():
    products = Product.query.all()
    return jsonify(
        [
            {
                "id": product.id,
                "name": product.name,
                "manufacturer": product.manufacturer,
                "accords": [accord.name for accord in product.accords],
                "reviews": [
                    {"rating": review.rating, "content": review.content}
                    for review in product.review
                ],
            }
            for product in products
        ]
    )

@product_blueprint.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "manufacturer": product.manufacturer,
            "accords": [accord.name for accord in product.accords],
            "reviews": [
                {"rating": review.rating, "content": review.content}
                for review in product.reviews
            ],
        }
    )

@product_blueprint.route("/add_product", methods=["POST"])
def add_product():
    try:
        data = request.json
        new_product = Product(
            name=data["name"],
            manufacturer=data.get("manufacturer"),
        )
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
                    "manufacturer": new_product.manufacturer,
                    "accords": [accord.name for accord in new_product.accords],
                },
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_blueprint.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get("name", product.name)
    product.manufacturer = data.get("manufacturer", product.manufacturer)
    db.session.commit()
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "manufacturer": product.manufacturer,
        }
    )

@product_blueprint.route("/add_review/<int:product_id>", methods=["POST"])
def add_review(product_id):
    try:
        data = request.json

        # Validate incoming data
        if "rating" not in data or "content" not in data:
            return jsonify({"error": "Both 'rating' and 'content' are required"}), 400

        # Check that rating is an integer
        if not isinstance(data["rating"], int):
            return jsonify({"error": "'rating' must be an integer"}), 400

        # Find the product ID
        product = Product.query.get_or_404(product_id)

        # Create a new review
        new_review = Review(
            rating=data["rating"], content=data["content"], product_id=product.id
        )

        # Add the review to the product's review relationship
        db.session.add(new_review)
        db.session.commit()

        return jsonify(
            {
                "review_id": new_review.id,
                "product_id": new_review.product_id,
            }
        ), 200

    except Exception as e:
        print(f"Error adding review: {e}")  # Add detailed logging for debugging
        return jsonify({"error": str(e)}), 400


@product_blueprint.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

# ----------------------------- #
#           ACCORDS             #
# ----------------------------- #

@product_blueprint.route("/accords", methods=["GET"])
def list_accords():
    accords = Accord.query.all()
    return jsonify([{"id": accord.id, "name": accord.name} for accord in accords])