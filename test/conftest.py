import pytest


@pytest.fixture
def api_base_url():
    # return "http://localhost:8000/"
    return "http://api-gateway:8000"


@pytest.fixture
def mock_api_response(mocker):
    def _mock_response(status_code, json_data):
        mock_resp = mocker.Mock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

    return _mock_response
