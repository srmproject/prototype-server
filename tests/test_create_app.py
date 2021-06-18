from app import create_app
import pytest

def test_app():
    app = create_app(mode='Test')
    # app.url_map.strict_slashes = False

    client = app.test_client()
    url = "/api/v1/index/"

    response = client.get(url)
    assert response.status_code == 200