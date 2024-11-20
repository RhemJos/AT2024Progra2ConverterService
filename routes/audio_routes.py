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
from converters.audio_to_audio.audio_converter import AudioConversionError
import os

audio_blueprint = Blueprint('convert-audio', __name__)  # Create a Blueprint for audio conversion-related routes


# Route: Audio Conversion Microservice
@audio_blueprint.route('/convert-audio', methods=['POST'])
def convert_audio():  # Extract parameters from the incoming form data
    output_format = request.form.get('output_format', 'mp3')  # Default to mp3 if no format specified
    bit_rate = request.form.get('bit_rate')  # Optional parameter for audio bit rate
    channels = request.form.get('channels')  # Optional parameter for audio channels (mono/stereo)
    sample_rate = request.form.get('sample_rate')  # Optional sample rate
    volume = request.form.get('volume')  # Optional volume adjustment
    language_channel = request.form.get('language_channel')  # Optional language channel for multi-language audio
    speed = request.form.get('speed')  # Optional speed adjustment for the audio
    # Attempt to save the uploaded audio file
    try:  # Save audio file to the specified directory
        output_path = save_file(request, 'audio', 'audio_converted_outputs')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400  # If file saving fails, return a 400 error with the message

    # Save or retrieve from DB
    try:  # Attempt to save or retrieve the file from a database
        file_in_db, file = get_or_save(output_path)  # Save the file in DB or retrieve it if it exists
    except Exception as e:
        return jsonify({"error": f"Failed to save file to DB: {str(e)}"})  # Return error if database saving fails
    # Create an instance of the AudioConverter with the file path
    converter = AudioConverter(file.file_path)
    # Prepare the arguments dictionary for the conversion process
    kwargs = {}
    if bit_rate:
        kwargs['bit_rate'] = bit_rate  # If bit_rate is provided, add it to the arguments
    if channels:
        kwargs['channels'] = channels  # If channels are specified, include them
    if sample_rate:
        kwargs['sample_rate'] = sample_rate  # If sample_rate is specified, include it
    if volume:
        kwargs['volume'] = volume  # If volume is specified, include it
    if language_channel:
        kwargs['language_channel'] = language_channel  # If language_channel is specified, include it
    if speed:
        kwargs['speed'] = speed  # If speed is specified, include it
    # Attempt to convert the audio file
    try:  # Perform the conversion with the provided arguments
        converted_output_path = converter.convert(output_format, **kwargs)
    except AudioConversionError as error:  # Return custom error message if conversion fails
        return jsonify({"error": error.get_message()}), error.get_status_code()
    except Exception as e:
        return jsonify({"error": "Audio conversion failed."}), 500  # General error if an exception occurs
    # Construct the URL for downloading the converted audio file
    download_url = (request.host_url + 'api/download-audio/'
                    + os.path.splitext(os.path.basename(converted_output_path))[0] + '.' + output_format)
    # Return the success message with the download URL
    if converted_output_path:
        return jsonify({"message": "Audio converted successfully.",
                        "download_URL": download_url
                        }), 200  # Success response with download URL
    else:
        return jsonify({"error": "Audio conversion failed."}), 500  # If conversion failed, return error
