from http import HTTPStatus

from app import db

from ..model.BlackList import BlacklistToken


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {"status": "success", "message": "Successfully logged out."}
        return response_object, HTTPStatus.OK
    except Exception as e:
        response_object = {"status": "fail", "message": e}
        return response_object, HTTPStatus.OK
