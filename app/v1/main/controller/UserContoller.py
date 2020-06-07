from http import HTTPStatus

from flask_restplus import Namespace, Resource

from app.exceptions import FieldValidationException
from app.v1 import v1_api
from app.v1.main.model.UserModel import User
from app.v1.main.service.UserService import UserService
from utils.decorators import admin_token_required, token_required

ls_user_ns = Namespace("user")


@ls_user_ns.route("/")
class UserList(Resource):
    user_service = UserService()

    @ls_user_ns.marshal_with(
        User.get_user_response_model,
        code=HTTPStatus.OK,
        as_list=True,
        description="Get all users",
        envelope="users",
    )
    @admin_token_required
    def get(self):
        users = self.user_service.get_all_users()
        return users, HTTPStatus.OK

    @ls_user_ns.doc(body=User.create_user_request_model, validate=True)
    @ls_user_ns.marshal_with(
        User.create_user_response_model,
        code=HTTPStatus.CREATED,
        description="Create new user",
    )
    @token_required
    def post(self):
        payload = v1_api.payload
        user, exceptions = self.user_service.create_user(payload)
        if exceptions:
            raise FieldValidationException(exceptions)
        else:
            return user, HTTPStatus.CREATED
