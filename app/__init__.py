from flask import Flask
from .routes import blueprint
from .models import db
import os
from dotenv import load_dotenv

# function to initialize app and sqlite db
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trip_planner.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    app.register_blueprint(blueprint)

    with app.app_context():
        db.create_all()

    return app

# loading address and port from env file
load_dotenv()
def get_adress_and_port():
    app_address = os.getenv("ADDRESS", "127.0.0.1")
    app_port = int(os.getenv("PORT", "5000"))
    return [app_address, app_port]

    