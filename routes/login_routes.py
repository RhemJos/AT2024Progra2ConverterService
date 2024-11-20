#
# @login.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Blueprint, request, jsonify
from login_authenticator.authentication import LoginService

login_blueprint = Blueprint('login_routes', __name__)  # Create a Blueprint for login-related routes


@login_blueprint.route('/login', methods=['POST'])  # Route for user login
def login():  # Get authentication data from the request JSON
    authentication = request.json  # Validate presence of username and password in the request
    if not authentication or 'username' not in authentication or 'password' not in authentication:
        return jsonify({'message': 'Missing credentials!'}), 401  # Return error for incomplete credentials
    # Extract username and password from the request
    username = authentication['username']
    password = authentication['password']
    # Create an instance of the authentication service
    auth_service = LoginService()
    return auth_service.authenticate(username, password)  # Call the authentication service and return its response
