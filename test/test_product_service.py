import requests

BASE_URL = "http://localhost:5000"

def test_home():
    """Test the home route of the product service."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["message"] == "Product Service launched"
    print("Test Home Route: PASSED")

def test_add_product():
    """Test adding a new product."""
    product_data = {
        "name": "Test Fragrance",
        "designer": "Test Designer",
        "note": ["Bergamot", "Lavender"],
        "accords": ["Citrus", "Floral"]
    }
    response = requests.post(f"{BASE_URL}/add_product", json=product_data)

    # Print response for debugging
    print("Response:", response.json())

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    data = response.json()
    assert data["name"] == "Test Fragrance", f"Expected 'Test Fragrance', got {data['name']}"
    assert data["designer"] == "Test Designer", f"Expected 'Test Designer', got {data['designer']}"
    print("Test Add Product: PASSED")


def test_list_products():
    """Test listing all products."""
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert len(data) > 0, "No products found"
    print("Test List Products: PASSED")

def test_get_product():
    """Test retrieving a product by ID."""
    # Add a product first
    product_data = {
        "name": "Product to Retrieve",
        "designer": "Designer"
    }
    add_response = requests.post(f"{BASE_URL}/add_product", json=product_data)
    product_id = add_response.json()["id"]

    # Retrieve the product
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["name"] == "Product to Retrieve", f"Expected 'Product to Retrieve', got {data['name']}"
    print("Test Get Product: PASSED")

def test_delete_product():
    """Test deleting a product by ID."""
    # Add a product first
    product_data = {
        "name": "Product to Delete",
        "designer": "Designer"
    }
    add_response = requests.post(f"{BASE_URL}/add_product", json=product_data)
    product_id = add_response.json()["id"]

    # Delete the product
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["message"] == "Product deleted successfully"
    print("Test Delete Product: PASSED")

def test_add_product_missing_fields():
    """Test adding a product with missing fields."""
    product_data = {
        "designer": "No Name Designer"
    }
    response = requests.post(f"{BASE_URL}/add_product", json=product_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "error" in response.json(), "Error message missing in response"
    print("Test Add Product with Missing Fields: PASSED")

def test_add_product_long_name():
    """Test adding a product with a long name."""
    long_name = "a" * 101  # 101 characters, exceeding the limit
    product_data = {
        "name": long_name,
        "designer": "Test Designer"
    }
    response = requests.post(f"{BASE_URL}/add_product", json=product_data)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "error" in response.json(), "Error message missing in response"
    print("Test Add Product with Long Name: PASSED")


if __name__ == "__main__":
    test_home()
    test_add_product()
    test_list_products()
    test_get_product()
    test_delete_product()
    test_add_product_missing_fields()
    test_add_product_long_name()
