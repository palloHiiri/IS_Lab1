import os

from flask import Flask
from dotenv import load_dotenv

from app.database import init_db
from app.auth import init_security

from app.routes import api


def create_app():
    load_dotenv()

    app = Flask(__name__)

    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError(
            "JWT_SECRET_KEY is not configured"
        )

    app.config["JWT_SECRET_KEY"] = secret_key

    init_security(app)
    init_db()
    app.register_blueprint(api)
    return app