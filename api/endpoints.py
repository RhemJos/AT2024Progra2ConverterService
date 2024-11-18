import os
from flask import Blueprint, request, jsonify, send_file
from converters.video_to_images.video_to_images import VideoToImagesConverter
from converters.video_to_video.video_to_video import VideoToVideoConverter
from converters.image_to_image.image_converter import ImageConverter, IMAGE_OPTIONS
from converters.audio_to_audio.audio_converter import AudioConverter
from converters.extractor.metadataextractor import MetadataExtractor
from exceptions.image_convert_exception import ImageConvertError
from exceptions.video_convert_exception import VideoConvertError
from exceptions.audio_convert_exception import AudioConvertError
from converters.compressor.compressor import FolderCompressor
from helpers.endpoints_helper import save_file, get_or_save, update
from PIL import Image
import mimetypes
import io
from models import db, File
import hashlib


api = Blueprint('api', __name__)
# Video Converter - Microservice


@api.route('/video-to-images', methods=['POST'])
def video_to_images():  
    try:
        video_path = save_file(request, 'file', 'video_to_frames_outputs')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    try:
        file_in_db, file = get_or_save(video_path)
    except Exception as e:
        return jsonify({"error": f"Saving file in db failed: {str(e)}"})

    if file_in_db and file.output_path:
        os.remove(video_path)
        zip_url = request.host_url + '/api/download-frames/' + file.checksum + '.zip'
        return jsonify({
            "message": "Video ya existe en Base de Datos.",
            "output_path": '/' + file.output_path,
            "download_URL": zip_url.replace("\\", "/"),
        })

    converter = VideoToImagesConverter(file.file_path)
    try:
        converter.convert(fps=1)
    except VideoConvertError as e:
        return jsonify({"message": e.get_message()}), e.get_status_code()

    filename = os.path.splitext(os.path.basename(file.file_path))[0]
    frames_folder = os.path.join('outputs', 'video_to_frames_outputs', filename).replace("\\", "/")

    # Update output_path in DB
    file.output_path = frames_folder
    update(file)

    compressed_file = FolderCompressor(frames_folder)
    zip_path = compressed_file.compress()
    zip_url = request.host_url + '/api/download-frames/' + filename + '.zip'

    return jsonify({
        "message": "Video procesado con éxito.",
        "output_path": '/' + frames_folder,
        "download_URL": zip_url.replace("\\", "/"),
    })

@api.route('/video-to-video', methods=['POST'])
def video_to_video():
    try:
        # Guardar el archivo utilizando la función save_file
        video_path = save_file(request, 'file', 'video_to_video_outputs', valid_formats=["mp4", "mov", "avi", "mkv", "flv", "webm", "ogg", "wmv"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    fps = request.form.get('fps')
    output_format = request.form.get('format')
    vcodec = request.form.get('vcodec')
    acodec = request.form.get('acodec')
    audio_channels = request.form.get('audio_channels')


    # Save or retrieve from DB
    try:
        file_in_db, file = get_or_save(video_path)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo en DB: {str(e)}"})

    # Conversión del video
    converter = VideoToVideoConverter(file.file_path)

    try:
        converter.convert(
            output_format=output_format,
            fps=fps,
            video_codec=vcodec,
            audio_codec=acodec,
            audio_channels=audio_channels
        )
    except VideoConvertError as e:
        return jsonify({"message": e.get_message()}), e.get_status_code()

    filename = os.path.splitext(os.path.basename(file.file_path))[0]
    video_path_converted = os.path.join('outputs', 'video_to_video_outputs', f"{filename}.{output_format}")
    download_url = request.host_url + 'api/download-video/' + filename + '.' + output_format

    return jsonify({
        "message": "Video procesado con éxito.",
        "output_path": '/' + video_path_converted.replace("\\", "/"),
        "download_URL": download_url
    }), 200

@api.route('/download-frame/<foldername>/<filename>', methods=['GET'])
def download_frame(foldername, filename):
    folder = os.path.join('outputs', 'video_to_frames_outputs', foldername)
    frame_path = os.path.join(folder, filename)
    if os.path.exists(frame_path):
        return send_file(frame_path, as_attachment=True, download_name=f"{foldername}_{filename}")
    return jsonify({"error": "File not found"}), 404


@api.route('/download-frames/<filename>', methods=['GET'])
def download_frames(filename):
    frames_zip = os.path.join('outputs', 'video_to_frames_outputs', filename)
    if os.path.exists(frames_zip):
        return send_file(frames_zip, as_attachment=True)
    return jsonify({"error": "Folder not found"}), 404


@api.route('/download-video/<filename>', methods=['GET'])
def download_video(filename):
    video_folder = os.path.join('outputs', 'video_to_video_outputs')
    video_path = os.path.join(video_folder, filename)

    if os.path.exists(video_path):
        return send_file(video_path, as_attachment=True, download_name=filename)
    return jsonify({"error": "File not found"}), 404


# Image Converter - Microservice
@api.route('/image-configuration', methods=['POST'])
def image_configuration():
    try:
        image_path = save_file(request, 'image', 'image_converted_outputs', IMAGE_OPTIONS['extension'])
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    # Save or retrieve from DB
    try:
        file_in_db, file = get_or_save(image_path)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo en DB: {str(e)}"})

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
        return jsonify({"message": e.get_message()}), e.get_status_code()
    download_url = request.host_url + '/api/download-image/' + os.path.basename(output_path)
    return jsonify({
        "message": "Imagen procesada y guardada con éxito.",
        "output_path": "/" + output_path.replace("\\", "/"),
        "download_URL": download_url}), 200


@api.route('/download-image/<filename>', methods=['GET'])
def download_image(filename):
    image_folder = os.path.join('outputs', 'image_converted_outputs')
    image_path = os.path.join(image_folder, filename)

    if os.path.exists(image_path):
        return send_file(image_path, as_attachment=True, download_name=filename)
    return jsonify({"error": "File not found"}), 404


# Audio Converter - Microservice

@api.route('/convert-audio', methods=['POST'])
def convert_audio():    
    output_format = request.form.get('output_format', 'mp3')  # Formato predeterminado
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
        return jsonify({"error": f"No se pudo guardar el archivo en DB: {str(e)}"})

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
        return jsonify({"message": e.get_message()}), e.get_status_code()


    download_url = (request.host_url + 'api/download-audio/'
                    + os.path.splitext(os.path.basename(file.file_path))[0] + '.' + output_format)

    if converted_output_path:
        return jsonify({"message": "Audio convertido con éxito.",
                        "output_path": '/' + converted_output_path.replace("\\", "/"),
                        "download_URL": download_url
                        }), 200
    else:
        return jsonify({"error": "Conversión de audio fallida."}), 500

@api.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    audio_folder = os.path.join('outputs', 'audio_converted_outputs')
    audio_path = os.path.join(audio_folder, filename)

    if os.path.exists(audio_path):
        return send_file(audio_path, as_attachment=True, download_name=filename)
    return jsonify({"error": "File not found"}), 404

# Meda data extractor - Microservice
@api.route('/get-metadata', methods=['POST'])
def get_metadata():
    try:
        file_path = save_file(request, 'file', 'metadata_outputs')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    meta_data_extractor = MetadataExtractor(file_path)
    result = meta_data_extractor.extract()

    os.remove(file_path)

    return jsonify(result)