import os
from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", app.config["JWT_SECRET_KEY"])
    JWTManager(app)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app

