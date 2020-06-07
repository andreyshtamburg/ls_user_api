import uuid

from werkzeug.security import generate_password_hash

from app import db, flask_bcrypt
from app.v1.main.model.UserModel import User


class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def create_user(self, payload):
        hashed_password = flask_bcrypt.generate_password_hash(
            payload["password"]
        ).decode("utf-8")
        exception_map = {}
        user = self.get_user_by_email(payload["email"])
        if not user:
            user = User(
                email=payload["email"],
                first_name=payload["first_name"].lower().capitalize(),
                last_name=payload["last_name"].lower().capitalize(),
                password_hash=hashed_password,
                uuid=str(uuid.uuid4()),
                admin=True,
            )
            db.session.add(user)
            db.session.commit()
        else:
            exception_map[
                "user_already_exists"
            ] = f'user with email \'{payload["email"]}\' already exists'
        return user, exception_map
