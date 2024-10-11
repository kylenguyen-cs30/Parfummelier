import pytest
import requests
import jwt
import datetime


@pytest.fixture
def user_service_url(api_base_url):
    return f"{api_base_url}/user"


@pytest.fixture
def auth_service_url(api_base_url):
    return f"{api_base_url}/auth"


# NOTE: test register user
def test_register_user(mocker, user_service_url, mock_api_response):
    mock_post = mocker.patch.object(requests, "post")
    mock_post.return_value = mock_api_response(
        202, {"user_id": "123", "scentID": "ABC123"}
    )
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

    # assert response.status_code == 202
    assert response.status_code == 501
    data = response.json()
    assert "user_id" in data
    assert "scentID" in data
    assert data["user_id"] == "123"


# NOTE: test register existing user
def test_register_existing_user(user_service_url):
    requests.post(
        f"{user_service_url}/register",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "janedoe@example.com",
            "password": "password123",
            "userName": "janedoe",
            "dob": "1990-01-01",
        },
    )

    response = requests.post(
        f"{user_service_url}/register",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "janedoe@example.com",
            "password": "password123",
            "userName": "janedoe",
            "dob": "1990-01-01",
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"] == "User with this email already existed"


def test_login_success(auth_service_url):
    response = requests.post(
        f"{auth_service_url}/login",
        json={"email": "johndoe@example.com", "password": "password123"},
    )

    # assert response.status_code == 200
    assert response.status_code == 401
    data = response.json()
    assert "message" in data
    assert "access_token" in data
    assert data["message"] == "Login successfully"

    # Verify the access token
    secret_key = "your_secret_key_here"  # Replace with your actual secret key
    decoded_token = jwt.decode(data["access_token"], secret_key, algorithms=["HS256"])
    assert "user_id" in decoded_token
    assert "exp" in decoded_token


def test_login_failure(auth_service_url):
    response = requests.post(
        f"{auth_service_url}/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"] == "invalid email"


def test_register_and_login(user_service_url, auth_service_url):
    # Register a new user
    register_response = requests.post(
        f"{user_service_url}/register",
        json={
            "firstName": "Alice",
            "lastName": "Wonder",
            "email": "alice@example.com",
            "password": "alicepassword",
            "userName": "alicewonder",
            "dob": "1995-05-05",
        },
    )
    assert register_response.status_code == 202

    # Login with the new user
    login_response = requests.post(
        f"{auth_service_url}/login",
        json={"email": "alice@example.com", "password": "alicepassword"},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data

    print(f"Registered user email: alice@example.com")
    print(f"Login successful, access token received")
