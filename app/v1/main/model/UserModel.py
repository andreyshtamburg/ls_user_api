from datetime import datetime, timedelta

import jwt
from flask_restplus import fields

from app import db, flask_bcrypt
from app.v1 import v1_api
from app.v1.main.model.BlackList import BlacklistToken
from config import key


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    uuid = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1, seconds=5),
                "iat": datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, key, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            else:
                return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    get_user_response_model = v1_api.model(
        "User",
        {
            "uuid": fields.String,
            "email": fields.String,
            "first_name": fields.String,
            "last_name": fields.String,
            "admin": fields.Boolean,
            "created_at": fields.DateTime,
        },
    )

    create_user_response_model = v1_api.model("User", {"uuid": fields.String,})

    create_user_request_model = v1_api.model(
        "Create User Request Model",
        {
            "email": fields.String,
            "password": fields.String,
            "first_name": fields.String,
            "last_name": fields.String,
        },
    )

    login_user_request_model = v1_api.model(
        "User", {"email": fields.String, "password": fields.String}
    )

    def __repr__(self):
        return "<User '{}'>".format(self.username)
