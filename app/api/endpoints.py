import os
from flask import Blueprint, request, jsonify, send_file
from ..converters.video_to_images.video_converter import VideoConverter
from ..converters.extractor.metadataextractor import MetadataExtractor

api = Blueprint('api', __name__)

# Video Converter - Microservice

@api.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No se ha enviado ningun 'file' en la solicitud."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se ha seleccionado ningún archivo."})

    video_folder = os.path.join('app', 'converters', 'video_to_images', 'videos')
    os.makedirs(video_folder, exist_ok=True)
    video_path = os.path.join(video_folder, file.filename)

    file.save(video_path)

    converter = VideoConverter(video_path)
    converter.to_frames()

    os.remove(video_path)

    return jsonify({"message": "Video procesado con éxito."})


@api.route('/download-frames/<filename>', methods=['GET'])
def download_frames(filename):
    zip_path = os.path.join('app', 'converters', 'video_to_images', 'outputs', f"{filename}_frames.zip")
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)

    return jsonify({"error": "File not found"}), 404

# Extractor microservice

@api.route('/extractor/get-metadata', methods=['POST'])
def get_metadata():
    if 'file_path' not in request.form:
        return jsonify({"error": "No se ha enviado ningun 'file' en la solicitud."})
    
    file_path = request.form["file_path"]
    meta_data_extractor = MetadataExtractor(file_path)
    result = meta_data_extractor.extract()
    return jsonify(result)
