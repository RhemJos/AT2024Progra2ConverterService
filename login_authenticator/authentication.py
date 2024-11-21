#
# @authentication.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import datetime
import jwt
from flask import jsonify, current_app
from login_authenticator.authenticator import AuthenticationService
from dotenv import load_dotenv
import os
from login_authenticator.ValidUsers import validate_user
load_dotenv()


class LoginService(AuthenticationService):

    def authenticate(self, username, password):
        # Verify credentials
        secret_key = os.getenv('JWT_SECRET_KEY')
        if not validate_user(username, password):  
            return jsonify({'message': 'Invalid credentials!'}), 401
        # Generate a JWT token
        print(username, password)
        token = jwt.encode({
            'username': username,
            'password': password,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, secret_key, algorithm='HS256')  

        return jsonify({'access_token': token}), 200

