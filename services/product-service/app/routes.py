from flask_migrate import branches
from flask import Blueprint, request, jsonify, send_from_directory
from app.models import db, Product, Accord, Review
import os


product_blueprint = Blueprint("product", __name__)

# NOTE:
# Define the path to images directory
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")
IMAGES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")


@product_blueprint.route("/images/<path:filename>")
def serve_image(filename):
    """
    serve images from the image directory
    """
    return send_from_directory(IMAGES_PATH, filename)


@product_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Product Service launched"}), 200


# ----------------------------- #
#           PRODUCTS            #
# ----------------------------- #


# NOTE: Full List Products return
@product_blueprint.route("/products", methods=["GET"])
def list_products():
    products = Product.query.all()
    # base_url = f"{API_GATEWAY_URL}/images/"  # Get the base URL for images
    base_url = "http://api-gateway:8000/images"  # PERF: testing
    return jsonify(
        [
            {
                "id": product.id,
                "name": product.name,
                "brand": product.brand,
                "accords": [
                    {"name": accord.name, "background_color": accord.background_color}
                    for accord in product.accords
                ],
                "imageURL": base_url + product.imageURL if product.imageURL else None,
            }
            for product in products
        ]
    )


# NOTE: Single product return
@product_blueprint.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    base_url = f"{API_GATEWAY_URL}/images/"  # Get the base URL for images
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "accords": [accord.name for accord in product.accords],
            "imageURL": base_url + product.imageURL if product.imageURL else None,
        }
    )


# NOTE: Add Product
@product_blueprint.route("/add_product", methods=["POST"])
def add_product():
    try:
        data = request.json
        new_product = Product(
            name=data["name"],
            brand=data["brand"],
            imageURL=data.get("imageURL"),
        )

        accord_objects = []
        for accord_data in data.get("accords", []):
            # Check if this is a dict with name and color or just a name string
            if isinstance(accord_data, dict):
                accord_name = accord_data["name"]
                background_color = accord_data.get("background_color")
            else:
                accord_name = accord_data
                background_color = None

            accord_obj = Accord.query.filter_by(name=accord_name).first()
            if not accord_obj:
                accord_obj = Accord(name=accord_name, background_color=background_color)
                db.session.add(accord_obj)
            elif background_color and not accord_obj.background_color:
                # Update background color if it's not set
                accord_obj.background_color = background_color

            accord_objects.append(accord_obj)

        new_product.accords = accord_objects
        db.session.add(new_product)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_product.id,
                    "name": new_product.name,
                    "brand": new_product.brand,
                    "accords": [
                        {
                            "name": accord.name,
                            "background_color": accord.background_color,
                        }
                        for accord in new_product.accords
                    ],
                    "imageURL": new_product.imageURL,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


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

        return (
            jsonify(
                {
                    "review_id": new_review.id,
                    "product_id": new_review.product_id,
                }
            ),
            200,
        )

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


# Recommendation Route
@product_blueprint.route("/recommendations", methods=["POST"])
def recommend_products():
    data = request.json
    accordbank = data.get("accordbank", [])

    if not accordbank:
        return jsonify({"error": "No accord bank data provided"}), 400

    # Query the database for products that match any accord in the accordbank
    recommended_products = (
        Product.query
        .join(Product.accords)
        .filter(Accord.name.in_(accordbank))
        .distinct()
        .all()
    )

    # Format the recommendations in JSON format
    recommendations = [
        {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "accords": [accord.name for accord in product.accords],
            "imageURL": f"{API_GATEWAY_URL}/product/images/{product.imageURL}"
            if product.imageURL
            else None,
        }
        for product in recommended_products
    ]

    return jsonify({"recommendations": recommendations})


# NOTE: Rating Routes
