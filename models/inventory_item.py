from database import db

class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price       = db.Column(db.Float, nullable=False, default=0.0)
    quantity    = db.Column(db.Integer, nullable=False, default=0)
    barcode     = db.Column(db.String(50), nullable=True)
    brand       = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "description": self.description,
            "price":       self.price,
            "quantity":    self.quantity,
            "barcode":     self.barcode,
            "brand":       self.brand,
        }

    def __repr__(self):
        return f"<InventoryItem {self.name}>"
