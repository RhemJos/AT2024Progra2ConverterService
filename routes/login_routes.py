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

login_blueprint = Blueprint('login_routes', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():
    authentication = request.json
    if not authentication or 'username' not in authentication or 'password' not in authentication:
        return jsonify({'message': 'Missing credentials!'}), 401

    username = authentication['username']
    password = authentication['password']

    auth_service = LoginService()
    return auth_service.authenticate(username, password)
