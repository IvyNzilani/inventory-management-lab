# Inventory Management Lab

A Flask REST API for managing inventory with OpenFoodFacts API integration and a CLI interface.

## Features
- Full CRUD for inventory items
- Fetch product details from OpenFoodFacts by barcode or name
- Add external products directly to inventory
- CLI interface to interact with the API
- Unit tested with pytest

## Setup
```bash
git clone https://github.com/YOUR_USERNAME/inventory-management-lab
cd inventory-management-lab
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Run CLI
```bash
python cli/cli.py
```

## Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | /items/ | Get all items |
| GET | /items/<id> | Get single item |
| POST | /items/ | Create item |
| PATCH | /items/<id> | Update item |
| DELETE | /items/<id> | Delete item |
| GET | /external/barcode/<barcode> | Fetch from OpenFoodFacts |
| GET | /external/search?name=<name> | Search OpenFoodFacts |
| POST | /external/barcode/<barcode>/add | Fetch and add to inventory |

## Run Tests
```bash
pytest tests/ -v
```
