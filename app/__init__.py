from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# This will now be used from config.py
from app.config import SQLALCHEMY_DATABASE_URI
from app.utils import login_required

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Set app configurations
    app.config['SECRET_KEY'] = 'SoilMarketKey123'
    app.config.from_pyfile('config.py')  # Loads configurations from config.py

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import and register blueprints here to avoid circular imports
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app
