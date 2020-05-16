from http import HTTPStatus

from flask_restplus import Resource, Namespace, abort

from app.v1.main.model.UserModel import User
from app.v1.main.service.UserService import UserService

ls_user_ns = Namespace('user')


@ls_user_ns.route('/')
class UserList(Resource):
    user_service = UserService()

    @ls_user_ns.marshal_with(User.get_user_response_model,
                             code=HTTPStatus.OK,
                             as_list=True,
                             description='Get all users',
                             envelope='users')
    def get(self):
        users = self.user_service.get_all_users()
        return users, HTTPStatus.OK
