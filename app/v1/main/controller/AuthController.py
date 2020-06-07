from flask import request
from flask_restplus import Namespace, Resource

from app.v1 import v1_api
from app.v1.main.model.UserModel import User
from app.v1.main.service.AuthHelper import Auth

ls_auth_ns = Namespace("auth")


@ls_auth_ns.route("/login")
class UserLogin(Resource):
    """User Login Resource"""

    @ls_auth_ns.doc("user login")
    @ls_auth_ns.expect(User.login_user_request_model, validate=True)
    def post(self):
        payload = v1_api.payload
        return Auth.login_user(data=payload)


@ls_auth_ns.route("/logout")
class UserLogout(Resource):
    """Logout Resource"""

    @ls_auth_ns.doc("logout a user")
    def post(self):
        auth_header = request.headers.get("Authorization")
        return Auth.logout_user(data=auth_header)
