#
# @test_video_routes.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import unittest
from unittest.mock import patch
from flask import Flask
from werkzeug.datastructures import FileStorage
from routes.metadata_routes import metadata_blueprint


class TestVideoRoutes(unittest.TestCase):
    def setUp(self):
        # Create Flask instance and register blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(metadata_blueprint)
        self.client = self.app.test_client()  # Test client
    def test_video_routes(self):
        pass