import pytest
from app import create_app
from database import db

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_all_empty(client):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json == []

def test_create_item(client):
    response = client.post("/items/", json={
        "name": "Milk", "description": "Fresh milk",
        "price": 1.99, "quantity": 50
    })
    assert response.status_code == 201
    assert response.json["name"] == "Milk"

def test_get_single_item(client):
    client.post("/items/", json={
        "name": "Bread", "price": 2.50, "quantity": 20
    })
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json["name"] == "Bread"

def test_update_item(client):
    client.post("/items/", json={
        "name": "Old Name", "price": 1.00, "quantity": 1
    })
    response = client.patch("/items/1", json={"name": "New Name", "price": 3.00})
    assert response.status_code == 200
    assert response.json["name"] == "New Name"

def test_delete_item(client):
    client.post("/items/", json={
        "name": "Delete Me", "price": 1.00, "quantity": 1
    })
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert "deleted" in response.json["message"]

def test_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404

def test_create_missing_name(client):
    response = client.post("/items/", json={"price": 1.00, "quantity": 1})
    assert response.status_code == 400

def test_create_missing_price(client):
    response = client.post("/items/", json={"name": "No Price", "quantity": 1})
    assert response.status_code == 400

def test_create_missing_quantity(client):
    response = client.post("/items/", json={"name": "No Quantity", "price": 1.00})
    assert response.status_code == 400
