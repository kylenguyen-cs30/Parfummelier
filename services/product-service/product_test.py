import json

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Product Service launched"}

def test_list_products_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json == []  # Expecting an empty list if there are no products

def test_add_product(client):
    data = {
        "name": "Test Product",
        "accords": ["Fresh", "Woody"],
        "manufacturer": "Oscar Hernandez"
    }
    response = client.post(
        "/add_product", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["name"] == "Test Product"
    assert sorted(response.json["accords"]) == sorted(["Fresh", "Woody"])

def test_get_product(client):
    # Create a product to retrieve
    data = {
        "name": "Test Product",
        "accords": ["Woody"],
        "manufacturer": "Oscar Hernandez"
    }
    client.post("/add_product", data=json.dumps(data), content_type="application/json")

    # Fetch the product by ID
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json["name"] == "Test Product"
    assert response.json["manufacturer"] == "Oscar Hernandez"
    assert "reviews" in response.json
    
def test_update_product(client):
    # Add a product to update
    data = {
        "name": "Old Name",
        "accords": ["Woody"],
        "manufacturer": "Oscar Hernandez"
    }
    client.post("/add_product", data=json.dumps(data), content_type="application/json")
    
    # Update the product's name
    update_data = {"name": "Updated Name"}
    response = client.put("/products/1", data=json.dumps(update_data), content_type="application/json")
    assert response.status_code == 200
    assert response.json["name"] == "Updated Name"

def test_add_review(client):
    # Add a product first
    data = {
        "name": "Review Product",
        "accords": ["Fresh"],
        "manufacturer": "Oscar Hernandez"
    }
    product_response = client.post("/add_product", data=json.dumps(data), content_type="application/json")
    assert product_response.status_code == 201  # Ensure product was created successfully

    # Add a review to the product
    review_data = {"rating": 5, "content": "Excellent fragrance!"}
    response = client.post("/add_review/1", data=json.dumps(review_data), content_type="application/json")
    
    # Validate the review response
    assert response.status_code == 200
    assert response.json["review_id"] is not None
    assert response.json["product_id"] == 1

def test_delete_product(client):
    # Add a product to delete
    data = {
        "name": "Delete Product",
        "accords": ["Oriental"],
        "manufacturer": "Oscar Hernandez"
    }
    client.post("/add_product", data=json.dumps(data), content_type="application/json")

    # Delete the product by ID
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.json["message"] == "Product deleted successfully"
