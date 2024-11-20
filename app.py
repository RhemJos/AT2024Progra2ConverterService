#
# @app.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Flask
from models import db
from os import environ

from routes.metadata_routes import metadata_blueprint
from routes.audio_routes import audio_blueprint
from routes.image_routes import image_blueprint
from routes.video_routes import video_blueprint
from routes.download_routes import download_blueprint
from routes.login_routes import login_blueprint
# Create Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')  # Configure database URI from environment variable
# Initialize SQLAlchemy with the app
db.init_app(app)
# Create all database tables within the app context
with app.app_context():
    db.create_all()
# Register blueprints for modular routing with a prefix
app.register_blueprint(metadata_blueprint, url_prefix='/api')
app.register_blueprint(audio_blueprint, url_prefix='/api')
app.register_blueprint(image_blueprint, url_prefix='/api')
app.register_blueprint(video_blueprint, url_prefix='/api')
app.register_blueprint(download_blueprint, url_prefix='/api')
app.register_blueprint(login_blueprint, url_prefix='/api')

# Run the app on host 0.0.0.0 at port 9090 with debug mode enabled
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=True)
