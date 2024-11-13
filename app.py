#
# @app.py Copyright (c) 2021 Jalasoft. # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

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
