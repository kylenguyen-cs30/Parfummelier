import pytest


# @pytest.fixture
# def user_service_url():
#     return "http://localhost:5001"
#
#
# @pytest.fixture
# def auth_service_url():
#     return "http://localhost:5002"


#
@pytest.fixture
def user_service_url():
    return "http://localhost:8000/user"


#
#
# @pytest.fixture
# def auth_service_url():
#     return "http://localhost:8000/auth"
#


# @pytest.fixture
# def user_service_url():
#     return "http://api-gateway:8000/user"
#


@pytest.fixture
def auth_service_url():
    return "http://api-gateway:8000/auth"
