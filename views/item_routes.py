from flask import Blueprint, request, jsonify
from services.item_service import ItemService

item_bp = Blueprint("items", __name__)

@item_bp.route("/", methods=["GET"])
def get_all():
    items = ItemService.get_all_items()
    return jsonify(items), 200

@item_bp.route("/<int:item_id>", methods=["GET"])
def get_one(item_id):
    item, error = ItemService.get_item(item_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(item), 200

@item_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    item, error = ItemService.create_item(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(item), 201

@item_bp.route("/<int:item_id>", methods=["PATCH"])
def update(item_id):
    data = request.get_json()
    item, error = ItemService.update_item(item_id, data)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(item), 200

@item_bp.route("/<int:item_id>", methods=["DELETE"])
def delete(item_id):
    result, error = ItemService.delete_item(item_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(result), 200
