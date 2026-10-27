from datetime import timedelta

from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


bcrypt = Bcrypt()
jwt = JWTManager()


def init_security(app):
    bcrypt.init_app(app)
    jwt.init_app(app)


def hash_password(password):
    return bcrypt.generate_password_hash(
        password
    ).decode("utf-8")


def verify_password(password_hash, password):
    return bcrypt.check_password_hash(
        password_hash,
        password
    )


def generate_token(user_id):
    return create_access_token(
        identity=str(user_id),
        expires_delta=timedelta(hours=1)
    )