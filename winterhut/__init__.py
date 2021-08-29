import os
import json
import logging.config

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()
logging.config.fileConfig("logger.cfg")


def create_app():
    app = Flask(__name__)
    conf_path = os.environ.get("APP_CONFIG_PATH")
    if not conf_path:
        raise ValueError("No 'APP_CONFIG_PATH' environmental value defined to use as configuration file.")
    app.config.from_file(conf_path, load=json.load)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from winterhut.models.User import User
    from winterhut.models.Post import Post

    from winterhut.main.routes import main
    from winterhut.users.routes import users
    from winterhut.posts.routes import posts
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app
