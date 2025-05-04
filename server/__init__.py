from flask import Flask
from flask_cors import CORS
from .items import items_bp, load_items
from .purchases import purchases_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(items_bp)
    app.register_blueprint(purchases_bp)
    load_items()
    return app
