from app.main import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "CI/CD learning app is running"


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
