import pytest
import requests


# 1. Test registering a user with full information
def test_register_user_with_full_info(user_service_url):
    response = requests.post(
        user_service_url,
        json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "dob": "1990-01-01",
            "userName": "johndoe",
        },
    )

    assert response.status_code == 202  # Assuming 202 for successful registration
    data = response.json()
    assert "message" in data
    assert data["message"] == "User created successfully!"


# 2. Test registering a user with a missing attribute
def test_register_user_with_missing_attribute(user_service_url):
    response = requests.post(
        user_service_url,
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "janedoe@example.com",
            # "password" is missing
            "dob": "1990-01-01",
            "userName": "janedoe",
        },
    )

    assert response.status_code == 400  # Assuming 400 for bad request
    data = response.json()
    assert "error" in data
    assert data["error"] == "Missing password field"  # Modify according to actual error


# 3. Test registering two users with the same email (should fail with 401)
def test_register_user_with_same_email(user_service_url):
    # First user registration
    response_1 = requests.post(
        user_service_url,
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "janedoe@example.com",
            "password": "password123",
            "dob": "1990-01-01",
            "userName": "janedoe",
        },
    )
    assert response_1.status_code == 202

    # Second user registration with the same email
    response_2 = requests.post(
        user_service_url,
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "janedoe@example.com",  # Same email
            "password": "password123",
            "dob": "1990-01-01",
            "userName": "janedoe2",
        },
    )
    assert response_2.status_code == 401  # Assuming 401 for existing user
    data = response_2.json()
    assert "error" in data
    assert data["error"] == "User with this email already existed"


# 4. Test registering two users with different emails but same firstName and lastName
def test_register_user_with_same_name_different_email(user_service_url):
    # First user registration
    response_1 = requests.post(
        user_service_url,
        json={
            "firstName": "Alice",
            "lastName": "Wonder",
            "email": "alice@example.com",
            "password": "alicepassword",
            "dob": "1995-05-05",
            "userName": "alicewonder",
        },
    )
    assert response_1.status_code == 202

    # Second user registration with the same firstName and lastName but different email
    response_2 = requests.post(
        user_service_url,
        json={
            "firstName": "Alice",
            "lastName": "Wonder",
            "email": "alice2@example.com",  # Different email
            "password": "alicepassword",
            "dob": "1995-05-05",
            "userName": "alicewonder2",
        },
    )
    assert response_2.status_code == 202  # Assuming 202 for successful registration
    data = response_2.json()
    assert "message" in data
    assert data["message"] == "User created successfully!"
