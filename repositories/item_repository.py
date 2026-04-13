from database import db
from models.inventory_item import InventoryItem

class ItemRepository:

    @staticmethod
    def get_all():
        return InventoryItem.query.all()

    @staticmethod
    def get_by_id(item_id):
        return InventoryItem.query.get(item_id)

    @staticmethod
    def create(name, description, price, quantity, barcode=None, brand=None):
        item = InventoryItem(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            barcode=barcode,
            brand=brand
        )
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def update(item_id, data):
        item = InventoryItem.query.get(item_id)
        if not item:
            return None
        if "name"        in data: item.name        = data["name"]
        if "description" in data: item.description = data["description"]
        if "price"       in data: item.price       = data["price"]
        if "quantity"    in data: item.quantity     = data["quantity"]
        if "barcode"     in data: item.barcode      = data["barcode"]
        if "brand"       in data: item.brand        = data["brand"]
        db.session.commit()
        return item

    @staticmethod
    def delete(item_id):
        item = InventoryItem.query.get(item_id)
        if not item:
            return None
        db.session.delete(item)
        db.session.commit()
        return item
