import pytest
import requests


def test_register_user():
    # Simulate sending a request to the /register endpoint
    response = requests.post(
        "http://user-service:5001/register",
        json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "userName": "johndoe",
            "dob": "1990-01-01",
        },
    )

    # Check that the response was successful
    assert response.status_code == 202
    assert response.json()["message"] == "User created successfully!"
