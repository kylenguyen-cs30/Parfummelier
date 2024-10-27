# import pytest
#
#
# @pytest.fixture
# def api_base_url():
#     return "http://localhost:8000/"
#     # return "http://api-gateway:8000"
#
#
# @pytest.fixture
# def mock_api_response(mocker):
#     def _mock_response(status_code, json_data):
#         mock_resp = mocker.Mock()
#         mock_resp.status_code = status_code
#         mock_resp.json.return_value = json_data
#         return mock_resp
#
#     return _mock_response
#


import pytest
import requests


@pytest.fixture
def api_url():
    # Use the provided base URL
    return "http://user-service:5000"


@pytest.fixture
def user_service_url(api_url):
    return f"{api_url}/register"

@pytest.fixture
def mock_api_response(mocker):
    def _mock_response(status_code, json_data):
        mock_resp = mocker.Mock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

    return _mock_response
