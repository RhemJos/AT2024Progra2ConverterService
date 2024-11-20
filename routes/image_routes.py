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
import os

image_blueprint = Blueprint('image_routes', __name__)  # Create a Blueprint for image-related routes


# Image Converter - Microservice
@image_blueprint.route('/image-configuration', methods=['POST'])
def image_configuration():
    try:  # Step 1: Save uploaded image file
        image_path = save_file(request, 'image', 'image_converted_outputs', VALID_IMAGE_EXTENSIONS)
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400  # Return error if file validation fails

    # Save or retrieve from DB
    try:  # Step 2: Save or retrieve the file from the database
        file_in_db, file = get_or_save(image_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save file to DB: {str(e)}"})

    try:  # Step 3: Instantiate the ImageConverter
        converter = ImageConverter(file.file_path)
    except ValueError:
        return jsonify({"error": "The image could not be loaded"}), 400
    # Step 4: Extract and parse optional image transformation parameters from the request
    resize_width = request.form.get('resize_width', type=int)  # Width for resizing
    resize_height = request.form.get('resize_height', type=int)  # Height for resizing
    resize_measures = (resize_width, resize_height) if resize_width or resize_height else None
    resize_type = request.form.get('resize_type', default=None)  # Resizing type (e.g., aspect ratio preservation)
    format = request.form.get('format', default=None)  # Target format for the output file
    rotate_angle = request.form.get('rotate', type=int)  # Rotation angle for the image
    grayscale = True if 'GRAYSCALE' in request.form else False  # Convert to grayscale if specified
    filters = []
    for filter in IMAGE_FILTERS:  # Collect applicable filters
        if filter in request.form:
            filters.append(filter)
    try:  # Step 5: Perform the image conversion with the parsed parameters
        output_path = converter.convert(resize=resize_measures, resize_type=resize_type, output_format=format,
                                        angle=rotate_angle, grayscale=grayscale, filters=filters)
    except ValueError as e:
        return jsonify({"message": e}), 400  # Handle any conversion errors
    # Step 6: Generate the download URL for the processed image
    download_url = request.host_url + '/api/download-image/' + os.path.basename(output_path)
    return jsonify({
        "message": "Image processed and saved successfully.",
        "download_URL": download_url}), 200
