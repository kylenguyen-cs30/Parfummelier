import pytest
from app import create_app, db
from app.models import Product, Accord

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use an in-memory database for tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_recommend_products(client):
    # Add sample accords and products to the database
    accord1 = Accord(name="Woody")
    accord2 = Accord(name="Amber")
    db.session.add(accord1)
    db.session.add(accord2)
    
    product1 = Product(name="Woody Scent", brand="TestBrand")
    product1.accords.extend([accord1, accord2])
    db.session.add(product1)
    db.session.commit()

    # Send a POST request to /recommendations with a sample accordbank
    response = client.post("/recommendations", json={"accordbank": ["Woody", "Amber"]})
    assert response.status_code == 200
    recommendations = response.get_json()["recommendations"]

    # Check if the correct products are recommended
    assert len(recommendations) == 1
    assert recommendations[0]["name"] == "Woody Scent"
    assert "Woody" in recommendations[0]["accords"]
