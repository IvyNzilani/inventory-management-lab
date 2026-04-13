import pytest
from unittest.mock import patch
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

def test_get_by_barcode_success(client):
    mock_product = {
        "name": "Nutella", "brand": "Ferrero",
        "description": "Hazelnut spread", "barcode": "3017620422003"
    }
    with patch("services.openfoodfacts_service.OpenFoodFactsService.get_by_barcode",
               return_value=(mock_product, None)):
        response = client.get("/external/barcode/3017620422003")
        assert response.status_code == 200
        assert response.json["name"] == "Nutella"

def test_get_by_barcode_not_found(client):
    with patch("services.openfoodfacts_service.OpenFoodFactsService.get_by_barcode",
               return_value=(None, "Product not found in OpenFoodFacts")):
        response = client.get("/external/barcode/0000000000")
        assert response.status_code == 404

def test_search_by_name_success(client):
    mock_results = [{"name": "Nutella", "brand": "Ferrero", "barcode": "3017620422003"}]
    with patch("services.openfoodfacts_service.OpenFoodFactsService.search_by_name",
               return_value=(mock_results, None)):
        response = client.get("/external/search?name=nutella")
        assert response.status_code == 200
        assert len(response.json) == 1

def test_search_missing_name(client):
    response = client.get("/external/search")
    assert response.status_code == 400

def test_fetch_and_add_success(client):
    mock_product = {
        "name": "Nutella", "brand": "Ferrero",
        "description": "Hazelnut spread", "barcode": "3017620422003"
    }
    with patch("services.openfoodfacts_service.OpenFoodFactsService.get_by_barcode",
               return_value=(mock_product, None)):
        response = client.post("/external/barcode/3017620422003/add",
                               json={"price": 4.99, "quantity": 10})
        assert response.status_code == 201
        assert response.json["item"]["name"] == "Nutella"

def test_fetch_and_add_not_found(client):
    with patch("services.openfoodfacts_service.OpenFoodFactsService.get_by_barcode",
               return_value=(None, "Product not found in OpenFoodFacts")):
        response = client.post("/external/barcode/0000000000/add",
                               json={"price": 1.00, "quantity": 1})
        assert response.status_code == 404
