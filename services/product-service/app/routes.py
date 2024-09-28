from flask import Blueprint, request, jsonify
from app.models import db, Product, Collection

product_blueprint = Blueprint('products', __name__)

# List all Available Products [For development]
@product_blueprint.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'designer': product.designer,
        'year_released': product.year_released,
        'collection': product.collection.name if product.collection else None
    } for product in products])

# List All product in a same collection_id
@product_blueprint.route('/collections/<int:collection_id>/products', methods=['GET'])
def list_products_by_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    products = Product.query.filter_by(collection_id=collection_id).all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'designer': product.designer,
        'year_released': product.year_released
    } for product in products])

# Return information of a product
@product_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'designer': product.designer,
        'year_released': product.year_released,
        'collection': product.collection.name if product.collection else None
    })

# Add new product
@product_blueprint.route('/products', methods=['POST'])
def add_product():
    data = request.json
    collection_id = data.get('collection_id')
    new_product = Product(
        name=data['name'],
        designer=data.get('designer'),
        year_released=data.get('year_released'),
        collection_id=collection_id
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({
        'id': new_product.id,
        'name': new_product.name,
        'designer': new_product.designer,
        'year_released': new_product.year_released,
        'collection': new_product.collection.name if new_product.collection else None
    }), 201

# Delete a product
@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

# Update a product
@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.designer = data.get('designer', product.designer)
    product.year_released = data.get('year_released', product.year_released)
    product.collection_id = data.get('collection_id', product.collection_id)
    db.session.commit()
    return jsonify({
        'id': product.id,
        'name': product.name,
        'designer': product.designer,
        'year_released': product.year_released,
        'collection': product.collection.name if product.collection else None
    })

# Create a new Collection
@product_blueprint.route('/collections', methods=['POST'])
def create_collection():
    data = request.json
    new_collection = Collection(
        name=data['name'],
        designer=data['designer']
    )
    db.session.add(new_collection)
    db.session.commit()
    return jsonify({
        'id': new_collection.id,
        'name': new_collection.name,
        'designer': new_collection.designer
    }), 201

# List all collections
@product_blueprint.route('/collections', methods=['GET'])
def list_collections():
    collections = Collection.query.all()
    return jsonify([{
        'id': collection.id,
        'name': collection.name,
        'designer': collection.designer
    } for collection in collections])