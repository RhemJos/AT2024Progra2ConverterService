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


class LoginService(AuthenticationService):

    def authenticate(self, username, password):
        # Verify credentials
        if username != 'Admin' or password != 'contraseña_123':  # Hard code
            return jsonify({'message': 'Credenciales inválidas!'}), 401
        # Generate a JWT token
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, 'default_secret_key', algorithm='HS256')  # Hard code

        return jsonify({'token': token}), 200

