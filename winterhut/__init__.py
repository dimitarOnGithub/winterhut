from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_file(config, load=json.load)

    db.init_app(app)
    from winterhut.models.User import User
    from winterhut.models.Post import Post

    from winterhut.main.routes import main
    app.register_blueprint(main)

    return app
