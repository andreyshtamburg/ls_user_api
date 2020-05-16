from datetime import datetime

from flask_restplus import fields

from app import db
from app.v1 import v1_api


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    uuid = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())
    password_hash = db.Column(db.String(128))

    get_user_response_model = v1_api.model('User', {
        'uuid': fields.String,
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'created_at': fields.DateTime
    })
