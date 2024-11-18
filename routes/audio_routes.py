#
# @audio_routes.py Copyright (c) 2021 Jalasoft.
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
from converters.audio_to_audio.audio_converter import AudioConverter
from exceptions.audio_convert_exception import AudioConvertError
import os

audio_blueprint = Blueprint('convert-audio', __name__)


# Audio Converter - Microservice
@audio_blueprint.route('/convert-audio', methods=['POST'])
def convert_audio():
    output_format = request.form.get('output_format', 'mp3')  # Default format
    bit_rate = request.form.get('bit_rate')
    channels = request.form.get('channels')
    sample_rate = request.form.get('sample_rate')
    volume = request.form.get('volume')
    language_channel = request.form.get('language_channel')
    speed = request.form.get('speed')

    try:
        output_path = save_file(request, 'audio', 'audio_converted_outputs')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    # Save or retrieve from DB
    try:
        file_in_db, file = get_or_save(output_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save file to DB: {str(e)}"})

    converter = AudioConverter(file.file_path)

    kwargs = {}
    kwargs['output_format'] = output_format
    if bit_rate:
        kwargs['bit_rate'] = bit_rate
    if channels:
        kwargs['channels'] = channels
    if sample_rate:
        kwargs['sample_rate'] = sample_rate
    if volume:
        kwargs['volume'] = volume
    if language_channel:
        kwargs['language_channel'] = language_channel
    if speed:
        kwargs['speed'] = speed

    try:
        converted_output_path = converter.convert(**kwargs)
    except AudioConvertError as e:
        return jsonify({"error": e.get_message()}), e.get_status_code()

    download_url = (request.host_url + 'api/download-audio/'
                    + os.path.splitext(os.path.basename(converted_output_path))[0] + '.' + output_format)

    if converted_output_path:
        return jsonify({"message": "Audio converted successfully.",
                        "output_path": '/' + converted_output_path.replace("\\", "/"),
                        "download_URL": download_url
                        }), 200
    else:
        return jsonify({"error": "Audio conversion failed."}), 500
