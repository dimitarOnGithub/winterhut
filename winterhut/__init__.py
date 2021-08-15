from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_file(config, load=json.load)

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
