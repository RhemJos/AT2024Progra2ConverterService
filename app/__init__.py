from flask import Flask
from .models import db, FilePath
from .routes import test_route


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_paths.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) 

    with app.app_context():
        db.create_all()

    app.register_blueprint(test_route)

    return app