#
# @metadata_routes.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Blueprint, request, jsonify
from helpers.endpoints_helper import save_file
from converters.extractor.metadataextractor import MetadataExtractor
import os

metadata_blueprint = Blueprint('get-metadata', __name__)


# Meda data extractor - Microservice
@metadata_blueprint.route('/get-metadata', methods=['POST'])
def get_metadata():
    try:
        file_path = save_file(request, 'file', 'metadata_outputs')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    meta_data_extractor = MetadataExtractor(file_path)
    result = meta_data_extractor.extract()
    os.remove(file_path)
    return jsonify(result)


