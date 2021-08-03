from fastapi.testclient import TestClient

from tar_api.app import app

client = TestClient(app)


def test_status_should_return_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
