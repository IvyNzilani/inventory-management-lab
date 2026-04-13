import pytest
from unittest.mock import patch, MagicMock
from cli.cli import view_all, add_item, delete_item

def test_view_all_empty():
    mock_response = MagicMock()
    mock_response.json.return_value = []
    with patch("requests.get", return_value=mock_response):
        view_all()

def test_view_all_with_items():
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "name": "Milk", "brand": "Brookside",
         "price": 1.99, "quantity": 10, "barcode": "123"}
    ]
    with patch("requests.get", return_value=mock_response):
        view_all()

def test_add_item_success():
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"name": "Milk"}
    with patch("requests.post", return_value=mock_response):
        with patch("builtins.input", side_effect=[
            "Milk", "Fresh milk", "1.99", "10", "Brookside", "123456"
        ]):
            add_item()

def test_delete_item_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Item 'Milk' deleted successfully"}
    with patch("requests.delete", return_value=mock_response):
        with patch("builtins.input", return_value="1"):
            delete_item()
