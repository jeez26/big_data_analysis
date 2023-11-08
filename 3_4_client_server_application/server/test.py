import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_server_data():
    response = client.get("/server/data")
    assert response.status_code == 200
    assert response.json() == {"message": "Server data!"}


def test_non_existing_route():
    response = client.get("/non-existing-route")
    assert response.status_code == 404
