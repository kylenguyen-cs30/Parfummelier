from app import db

# Create a Table for Collection Many-To-One Relationships
class Collection(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    designer = db.Column(db.String(100), nullable=False)
    
# TODO: Create a table for Product
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designer = db.Column(db.String(100), nullable=False)
    year_released = db.Column(db.Integer, nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=True)  # Foreign key to Collection
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# Connect the product with the Collection
    collection = db.relationship('Collection', backref='products')

# top_notes = db.Column(db.String(100))

