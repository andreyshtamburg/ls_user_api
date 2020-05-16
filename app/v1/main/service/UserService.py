from app.v1.main.model.UserModel import User


class UserService:

    @staticmethod
    def get_all_users():
        return User.query.all()
