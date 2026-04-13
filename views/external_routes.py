from flask import Blueprint, request, jsonify
from services.openfoodfacts_service import OpenFoodFactsService
from services.item_service import ItemService

external_bp = Blueprint("external", __name__)

@external_bp.route("/barcode/<barcode>", methods=["GET"])
def get_by_barcode(barcode):
    product, error = OpenFoodFactsService.get_by_barcode(barcode)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(product), 200

@external_bp.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name query parameter is required"}), 400
    results, error = OpenFoodFactsService.search_by_name(name)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(results), 200

@external_bp.route("/barcode/<barcode>/add", methods=["POST"])
def fetch_and_add(barcode):
    product, error = OpenFoodFactsService.get_by_barcode(barcode)
    if error:
        return jsonify({"error": error}), 404
    body = request.get_json() or {}
    product["price"]    = body.get("price", 0.0)
    product["quantity"] = body.get("quantity", 1)
    item, error = ItemService.create_item(product)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({
        "message": "Product fetched from OpenFoodFacts and added to inventory",
        "item":    item
    }), 201
