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


class LoginService(AuthenticationService):  # Define a subclass of AuthenticationService for login authentication
    # Implement the authenticate method required by the AuthenticationService abstract class
    def authenticate(self, username, password):
        # Verify credentials
        if username != 'Admin' or password != 'contraseña_123':  # Hardcoded (simplified for a first approach)
            return jsonify({'message': 'Invalid credentials!'}), 401  # Return an error message
        # If credentials are valid, generate a JWT (JSON Web Token)
        token = jwt.encode({
            'username': username,  # The username is stored in the token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Set the token expiration time to 1 hour
        }, 'default_secret_key', algorithm='HS256')  # Use a hardcoded secret key and the HS256 algorithm for signing
        # Return the generated JWT token as part of the response
        return jsonify({'token': token}), 200  # Return a success message with a 200 OK status

