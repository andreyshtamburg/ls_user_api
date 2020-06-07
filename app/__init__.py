from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# global object for SqlAlchemy
db = SQLAlchemy()
# global object for flask logging
logger = None
# global object for flask config
cfg = None
flask_bcrypt = Bcrypt()


def create_app(config_type="development"):
    """
    create flask application
    :param config_type: one of the following (development, testing, production)
    :return flask app object
    :rtype Flask
    """
    from config import config

    app = Flask(__name__)
    app.config.from_object(config[config_type])
    # Because of the bug in restplus.
    # https://github.com/noirbizarre/flask-restplus/issues/764
    app.config["PROPAGATE_EXCEPTIONS"] = False

    global cfg
    cfg = app.config

    db.init_app(app)

    from app.v1 import v1_blueprint

    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")

    return app
