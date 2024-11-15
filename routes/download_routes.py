#
# @download_routes.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Blueprint, jsonify, send_file
from helpers.endpoints_helper import send_file_download
import os

download_blueprint = Blueprint('download_routes', __name__)


@download_blueprint.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    return send_file_download('audio_converted_outputs', filename)


@download_blueprint.route('/download-image/<filename>', methods=['GET'])
def download_image(filename):
    return send_file_download('image_converted_outputs', filename)


@download_blueprint.route('/download-video/<filename>', methods=['GET'])
def download_video(filename):
    return send_file_download('video_converted_outputs', filename)


@download_blueprint.route('/download-frames/<filename>', methods=['GET'])
def download_frames(filename):
    return send_file_download('video_to_frames_outputs', filename, type_file="Folder")


@download_blueprint.route('/download-frame/<foldername>/<filename>', methods=['GET'])
def download_frame(foldername, filename):
    return send_file_download('video_to_frames_outputs', os.path.join(foldername, filename))

