import requests

# Base URLs for the services
user_service_url = "http://localhost:8000/user"
# user_service_url = "http://api-gateway:8000/user"
auth_service_url = "http://api-gateway:8000/auth"


# Test: Register user
def test_register_user():
    response = requests.post(
        f"{user_service_url}/register",
        json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "dob": "1990-01-01",
        },
    )
    print(f"Register Response: {response.json()}")  # Debugging the response
    assert response.status_code == 202, f"Expected 202, got {response.status_code}"
    data = response.json()
    assert "user_id" in data
    assert "scentID" in data
    return data["user_id"]


# Test: Login user
def test_login():
    response = requests.post(
        f"{auth_service_url}/login",
        json={
            "email": "johndoe@example.com",
            "password": "password123",
        },
    )
    print(f"Login Response: {response.json()}")  # Debugging the response
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "access_token" in data
    return data["access_token"]


# Main test sequence for register and login
def test_register_and_login():
    # Register user
    user_id = test_register_user()

    # Log in and get access_token
    access_token = test_login()

    print(f"Registered user ID: {user_id}")
    print(f"Access token: {access_token}")
