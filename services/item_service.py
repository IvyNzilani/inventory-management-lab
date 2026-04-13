from repositories.item_repository import ItemRepository

class ItemService:

    @staticmethod
    def get_all_items():
        items = ItemRepository.get_all()
        return [item.to_dict() for item in items]

    @staticmethod
    def get_item(item_id):
        item = ItemRepository.get_by_id(item_id)
        if not item:
            return None, "Item not found"
        return item.to_dict(), None

    @staticmethod
    def create_item(data):
        if not data.get("name"):
            return None, "Name is required"
        if data.get("price") is None:
            return None, "Price is required"
        if data.get("quantity") is None:
            return None, "Quantity is required"
        item = ItemRepository.create(
            name=data["name"],
            description=data.get("description", ""),
            price=data["price"],
            quantity=data["quantity"],
            barcode=data.get("barcode"),
            brand=data.get("brand")
        )
        return item.to_dict(), None

    @staticmethod
    def update_item(item_id, data):
        item = ItemRepository.update(item_id, data)
        if not item:
            return None, "Item not found"
        return item.to_dict(), None

    @staticmethod
    def delete_item(item_id):
        item = ItemRepository.delete(item_id)
        if not item:
            return None, "Item not found"
        return {"message": f"Item '{item.name}' deleted successfully"}, None
