import pytest


@pytest.fixture
def user_service_url():
    return "http://localhost:5001"


@pytest.fixture
def auth_service_url():
    return "http://localhost:5002"
