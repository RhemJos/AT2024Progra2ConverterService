import os
from flask import Blueprint, request, jsonify, send_file
from converters.video_to_images.video_converter import VideoConverter
from converters.image_to_image.image_converter import ImageConverter, IMAGE_FILTERS, VALID_IMAGE_EXTENSIONS
from converters.audio_to_audio.audio_converter import AudioConverter
from converters.extractor.metadataextractor import MetadataExtractor
from PIL import Image
import mimetypes
import io


api = Blueprint('api', __name__)

# Video Converter - Microservice

@api.route('/video-to-images', methods=['POST'])
def video_to_images():  
    try:
        video_path = save_file(request, 'file', 'video_to_frames_output')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    converter = VideoConverter(video_path)
    converter.to_frames()

    os.remove(video_path)

    filename = os.path.splitext(os.path.basename(video_path))[0]
    frames_folder = os.path.join('outputs', 'video_to_frames_output', filename)

    return jsonify({"message": "Video procesado con éxito.", "output_path": '/' + frames_folder.replace("\\", "/")})



@api.route('/video-to-video', methods=['POST'])
def video_to_video():    
    format = request.form.get('format')
    if format == '':
        return jsonify({"error": "No se ha seleccionado tipo de archivo a convertir."})

    try:
        video_path = save_file(request, 'file', 'video_to_frames_output')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400
    

    converter = VideoConverter(video_path)
    converter.convert_format(format)

    os.remove(video_path)

    filename = os.path.splitext(os.path.basename(video_path))[0]
    video_path_converted = os.path.join('outputs', 'video_converted_output', filename + '.' + format)

    return jsonify({"message": "Video procesado con éxito.", "video_path": '/' + video_path_converted.replace("\\", "/")})



@api.route('/download-frames/<filename>', methods=['GET'])
def download_frames(filename):
    frames_folder = os.path.join('outputs', 'video_to_frames_output', filename)
    
    if os.path.exists(frames_folder):
        return jsonify({"frames_folder_path": frames_folder})
    
    return jsonify({"error": "Folder not found"}), 404


@api.route('/download-video/<filename>', methods=['GET'])
def download_video(filename):
    video_folder = os.path.join('outputs', 'video_converted_output')
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
    try:
        image_path = save_file(request, 'image', 'image_converted_outputs', VALID_IMAGE_EXTENSIONS)
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400
    
    try:
        converter = ImageConverter(image_path)
    except ValueError:
        return jsonify({"error": "No fue posible cargar la imagen"}), 400


    # Obtener valores de resize, rotate y grayscale desde el formulario
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
        output_path = converter.convert(resize=resize_measures, resize_type=resize_type, format=format, 
                                        angle=rotate_angle, grayscale=grayscale, filters=filters)
    except ValueError as e:
        return jsonify({"message": e}), 400
    
    return jsonify({"message": "Imagen procesada y guardada con éxito.", "output_path": "/" + output_path.replace("\\", "/")}), 200



@api.route('/download-image/<filename>', methods=['GET'])
def download_image(filename):
    image_folder = os.path.join('outputs', 'image_converted_outputs')
    image_path = os.path.join(image_folder, filename)

    if os.path.exists(image_path):

        return jsonify({
            "image_path": image_path,
        })

    return jsonify({"error": "File not found"}), 404


# Audio Converter - Microservice

@api.route('/convert-audio', methods=['POST'])
def convert_audio():    
    output_format = request.form.get('output_format', 'mp3')  # Formato predeterminado
    bit_rate = request.form.get('bit_rate')
    channels = request.form.get('channels')
    sample_rate = request.form.get('sample_rate')
    volume = request.form.get('volume')
  
    try:
        audio_path = save_file(request, 'audio', 'audio_converted_outputs')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    converter = AudioConverter(audio_path)

    kwargs = {}
    if bit_rate:
        kwargs['bit_rate'] = bit_rate
    if channels:
        kwargs['channels'] = channels
    if sample_rate:
        kwargs['sample_rate'] = sample_rate
    if volume:
        kwargs['volume'] = volume

    converted_audio_path = converter.convert(output_format, **kwargs)

    if converted_audio_path:
        return jsonify({"message": "Conversión exitosa.", "converted_audio_path": '/' + converted_audio_path.replace("\\", "/")}), 200
    else:
        return jsonify({"error": "Conversión de audio fallida."}), 500


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


# Extracts file from request, check its extension(optional) and saves it in the corresponding dir
def save_file(request, file_type, dir, valid_formats=None):
    if file_type not in request.files:
        raise ValueError(f"No se ha enviado ningún archivo de {file_type} en la solicitud.")

    file = request.files[file_type]
    if file.filename == '':
        raise ValueError("No se ha seleccionado ningún archivo.")
    
    if valid_formats:
        extension = file.filename.split('.')[-1].lower()
        if extension not in valid_formats:
            raise ValueError(f"Formato de {file_type} no soportado.")

    file_folder = os.path.join('outputs', dir)
    os.makedirs(file_folder, exist_ok=True)

    file_path = os.path.join('outputs',  dir, file.filename)
    file.save(file_path)

    return file_path
