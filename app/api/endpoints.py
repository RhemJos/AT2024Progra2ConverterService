import os
import mimetypes
from flask import Blueprint, request, jsonify, send_file
from ..converters.video_to_images.video_converter import VideoConverter
from PIL import Image
import io


api = Blueprint('api', __name__)

# Video Converter - Microservice

@api.route('/video-to-images', methods=['POST'])
def video_to_images():
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



@api.route('/video-to-video', methods=['POST'])
def video_to_video():
    if 'file' not in request.files:
        return jsonify({"error": "No se ha enviado ningun 'file' en la solicitud."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se ha seleccionado ningún archivo."})
    
    format = request.form.get('format')
    if format == '':
        return jsonify({"error": "No se ha seleccionado tipo de archivo a convertir."})

    video_folder = os.path.join('app', 'converters', 'video_to_images', 'videos')
    os.makedirs(video_folder, exist_ok=True)
    video_path = os.path.join(video_folder, file.filename)

    file.save(video_path)

    converter = VideoConverter(video_path)
    converter.convert_format(format)

    os.remove(video_path)

    filename = os.path.splitext(os.path.basename(video_path))[0]
    video_path_converted = os.path.join('app', 'outputs', 'video_converted_output', filename + '.' + format)

    return jsonify({"message": "Video procesado con éxito.", "video_path": video_path_converted})



@api.route('/download-frames/<filename>', methods=['GET'])
def download_frames(filename):
    frames_folder = os.path.join('app', 'outputs', 'video_to_frames_output', filename)
    
    if os.path.exists(frames_folder):
        return jsonify({"frames_folder_path": frames_folder})
    
    return jsonify({"error": "Folder not found"}), 404


@api.route('/download-video/<filename>', methods=['GET'])
def download_video(filename):
    video_folder = os.path.join('app', 'outputs', 'video_converted_output')
    video_path = os.path.join(video_folder, filename)

    if os.path.exists(video_path):
        mime_type, _ = mimetypes.guess_type(video_path)

        return jsonify({
            "video_path": video_path,
            "mime_type": mime_type or "unknown"
        })

    return jsonify({"error": "File not found"}), 404


# Image Converter - Microservice


@api.route('/image-configuration', methods=['POST'])
def image_configuration():

    if 'image' not in request.files:
        return jsonify({"error": "No se encontró un archivo image."}), 400

    image_file = request.files['image']
    resize = request.form.get('resize', type=int)
    rotate = request.form.get('rotate', type=int)
    grayscale = request.form.get('grayscale', type=bool)

    image = Image.open(image_file)

    if resize:
        image = image.resize((resize, resize))

    if rotate:
        image = image.rotate(rotate, expand=True)

    if grayscale:
        image = image.convert("L")

    output_folder = os.path.join('app', 'outputs', 'image_converted_outputs')
    os.makedirs(output_folder, exist_ok=True) 

    output_filename = f"processed_image_{image_file.filename}"
    output_path = os.path.join(output_folder, output_filename)

    image.save(output_path)

    return jsonify({"message": "Imagen procesada y guardada con éxito.", "output_path": output_path}), 200



@api.route('/download-image/<filename>', methods=['GET'])
def download_image(filename):
    image_folder = os.path.join('app', 'outputs', 'image_converted_outputs')
    image_path = os.path.join(image_folder, filename)

    if os.path.exists(image_path):

        return jsonify({
            "image_path": image_path,
        })

    return jsonify({"error": "File not found"}), 404