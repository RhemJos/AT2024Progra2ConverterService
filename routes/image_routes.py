#
# @image_routes.py Copyright (c) 2021 Jalasoft.
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
from helpers.endpoints_helper import save_file, get_or_save
from converters.image_to_image.image_converter import ImageConverter, IMAGE_OPTIONS
from exceptions.image_convert_exception import ImageConvertError
import os

image_blueprint = Blueprint('image_routes', __name__)


# Image Converter - Microservice
@image_blueprint.route('/image-configuration', methods=['POST'])
def image_configuration():
    try:
        image_path = save_file(request, 'image', 'image_converted_outputs', IMAGE_OPTIONS['extension'])
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    # Save or retrieve from DB
    try:
        file_in_db, file = get_or_save(image_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save file to DB: {str(e)}"})

    try:
        converter = ImageConverter(file.file_path)
    except ImageConvertError as e:
        return jsonify({"error": e.args[0]}), 400

    resize_width = request.form.get('resize_width')
    resize_height = request.form.get('resize_height')
    resize_type = request.form.get('resize_type')
    format = request.form.get('output_format')
    rotate_angle = request.form.get('rotate')
    filters = request.form.getlist('filter')
    try:
        output_path = converter.convert(resize_width=resize_width, resize_height=resize_height, resize_type=resize_type, 
                                        output_format=format, angle=rotate_angle, filters=filters)
    except ImageConvertError as e:
        return jsonify({"error": e.get_message()}), e.get_status_code()

    download_url = request.host_url + '/api/download-image/' + os.path.basename(output_path)
    return jsonify({
        "message": "Image processed and saved successfully.",
        "output_path": "/" + output_path.replace("\\", "/"),
        "download_URL": download_url}), 200
