from functools import wraps

from flask import request
from flask_restplus import abort

from app.v1.main.service.AuthHelper import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            abort(status, data)

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get("data")
        print(f"token data is {token}")

        if not token:
            abort(status, data)

        admin = token.get("admin")
        if not admin:
            abort(401, "admin token required")

        return f(*args, **kwargs)

    return decorated
