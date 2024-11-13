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
from converters.image_to_image.image_converter import ImageConverter, IMAGE_FILTERS, VALID_IMAGE_EXTENSIONS

image_blueprint = Blueprint('image_routes', __name__)


# Image Converter - Microservice
@image_blueprint.route('/image-configuration', methods=['POST'])
def image_configuration():
    try:
        image_path = save_file(request, 'image', 'image_converted_outputs', VALID_IMAGE_EXTENSIONS)
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    # Save or retrieve from DB
    try:
        file_in_db, file = get_or_save(image_path)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo en DB: {str(e)}"})

    try:
        converter = ImageConverter(file.file_path)
    except ValueError:
        return jsonify({"error": "No fue posible cargar la imagen"}), 400

    resize_width = request.form.get('resize_width', type=int)
    resize_height = request.form.get('resize_height', type=int)
    resize_measures = (resize_width, resize_height) if resize_width or resize_height else None
    resize_type = request.form.get('resize_type', default=None)
    format = request.form.get('format', default=None)
    rotate_angle = request.form.get('rotate', type=int)
    grayscale = True if 'GRAYSCALE' in request.form else False
    filters = []
    for filter in IMAGE_FILTERS:
        if filter in request.form:
            filters.append(filter)
    try:
        output_path = converter.convert(resize=resize_measures, resize_type=resize_type, output_format=format,
                                        angle=rotate_angle, grayscale=grayscale, filters=filters)
    except ValueError as e:
        return jsonify({"message": e}), 400

    download_url = request.host_url + '/api/download-image/' + os.path.basename(output_path)
    return jsonify({
        "message": "Image processed and saved successfully.",
        "output_path": "/" + output_path.replace("\\", "/"),
        "download_URL": download_url}), 200

