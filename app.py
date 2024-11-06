from flask import Flask
# from models import db, FilePath
from routes import test_route
from api.endpoints import api


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_paths.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# with app.app_context():
#     db.create_all()

app.register_blueprint(test_route)
app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=True)
