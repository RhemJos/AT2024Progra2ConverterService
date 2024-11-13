from flask import Flask
from models import db
from routes import test_route
from api.endpoints import api
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(test_route)
app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=True)
