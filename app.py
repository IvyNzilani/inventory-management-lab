from flask import Flask
from database import db
from views.item_routes import item_bp
from views.external_routes import external_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(item_bp, url_prefix="/items")
    app.register_blueprint(external_bp, url_prefix="/external")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
