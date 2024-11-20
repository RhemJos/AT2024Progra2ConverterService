#
# @video_routes.py Copyright (c) 2021 Jalasoft.
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
from converters.video_to_video.video_to_video import VideoToVideoConverter
from converters.video_to_images.video_to_images import VideoToImagesConverter
from validators.VideoValidator import VideoValidator
from helpers.endpoints_helper import save_file, get_or_save, update
from helpers.compressor import FolderCompressor
import os

video_blueprint = Blueprint('video_routes', __name__)  # Create a Blueprint for video-related routes


# Video Converter - Microservice - Route for converting video to image frames
@video_blueprint.route('/video-to-images', methods=['POST'])
def video_to_images():
    try:  # Save uploaded video file and return its path
        video_path = save_file(request, 'file', 'video_to_frames_outputs')
    except ValueError as e:  # Return error if saving fails
        return jsonify({"error": e.args[0]}), 400

    try:  # Check or save the file in the database
        file_in_db, file = get_or_save(video_path)
    except Exception as e:  # Return error if saving to DB fails
        return jsonify({"error": f"Failed to save file to DB: {str(e)}"})

    if file_in_db and file.output_path:  # If file already processed, return existing download URL
        zip_url = request.host_url + '/api/download-frames/' + file.checksum + '.zip'
        return jsonify({
            "message": "Video already exists in Database.",
            "download_URL": zip_url.replace("\\", "/"),
        })
    # Initialize converter and process video frames at 1 FPS
    converter = VideoToImagesConverter(file.file_path)
    converter.convert(fps=1)
    # Define folder path for processed frames
    filename = os.path.splitext(os.path.basename(file.file_path))[0]
    frames_folder = os.path.join('outputs', 'video_to_frames_outputs', filename).replace("\\", "/")

    # Update output_path in DB
    file.output_path = frames_folder
    update(file)
    # Compress frames folder
    compressed_file = FolderCompressor(frames_folder)
    compressed_file.compress()
    zip_url = request.host_url + '/api/download-frames/' + filename + '.zip'
    # Return success message and download URL
    return jsonify({
        "message": "Video processed successfully.",
        "download_URL": zip_url.replace("\\", "/"),
    })


@video_blueprint.route('/video-to-video', methods=['POST'])  # Route for converting video to another video format
def video_to_video():
    try:  # Save uploaded video file with valid formats
        video_path = save_file(request, 'file', 'video_converted_outputs',
                               valid_formats=["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"])
    except ValueError as e:  # Return error if saving fails
        return jsonify({"error": str(e)}), 400
    fps = request.form.get('fps')  # Extract parameters from the request
    output_format = request.form.get('format')
    vcodec = request.form.get('vcodec')
    acodec = request.form.get('acodec')
    audio_channels = request.form.get('audio_channels')
    # Validate the parameters
    validation_errors = VideoValidator.validate(output_format, vcodec, acodec, fps, audio_channels)
    if validation_errors:
        return jsonify({"error": validation_errors}), 400
    # Save or retrieve from DB
    try:  # Check or save the file in the database
        file_in_db, file = get_or_save(video_path)
    except Exception as e:  # Return error if saving to DB fails
        return jsonify({"error": f"Failed to save file to DB: {str(e)}"})

    # Initialize converter and process video
    converter = VideoToVideoConverter(file.file_path)
    converter.convert(
        output_format=output_format,
        fps=fps,
        video_codec=vcodec,
        audio_codec=acodec,
        audio_channels=audio_channels
    )
    # Define converted video path and download URL
    filename = os.path.splitext(os.path.basename(file.file_path))[0]
    video_path_converted = os.path.join('outputs', 'video_converted_outputs', f"{filename}.{output_format}")
    download_url = request.host_url + 'api/download-video/' + filename + '-converted.' + output_format
    # Return success message and download URL
    return jsonify({
        "message": "Video processed successfully.",
        "download_URL": download_url
    }), 200
