import os
from flask import Blueprint, request, jsonify, send_file
from sqlalchemy.sql.coercions import expect
from converters.video_to_images.video_converter import VideoConverter
from converters.image_to_image.image_converter import ImageConverter, IMAGE_FILTERS, VALID_IMAGE_EXTENSIONS
from converters.audio_to_audio.audio_converter import AudioConverter
from converters.extractor.metadataextractor import MetadataExtractor
from validators.VideoValidator import VideoValidator
from converters.compressor.compressor import FolderCompressor
from models import db, File
from PIL import Image
import mimetypes
import io
import hashlib


api = Blueprint('api', __name__)
# Video Converter - Microservice


@api.route('/video-to-images', methods=['POST'])
def video_to_images():  
    try:
        video_path = save_file(request, 'file', 'video_to_frames_output')
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    try:
        file_in_db, new_path = get_or_save(video_path)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo en DB: {str(e)}"})
    
    if file_in_db:
        os.remove(video_path)
        return jsonify({"message": "Video ya existe.", "output_path": '/' + new_path.replace("\\", "/")})

    converter = VideoConverter(new_path)
    converter.to_frames()

    os.remove(new_path)

    filename = os.path.splitext(os.path.basename(new_path))[0]
    frames_folder = os.path.join('outputs', 'video_to_frames_output', filename).replace("\\", "/")

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
    if 'file' not in request.files:
        return jsonify({"error": "No se ha enviado ningun 'file' en la solicitud."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se ha seleccionado ningún archivo."})

    fps = request.form.get('fps')
    output_format = request.form.get('format')
    vcodec = request.form.get('vcodec')
    acodec = request.form.get('acodec')
    audio_channels = request.form.get('audio_channels')

    # Validación de parámetros
    validation_errors = VideoValidator.validate(output_format, vcodec, acodec, fps, audio_channels)
    if validation_errors:
        return jsonify({"error": validation_errors}), 400

    video_folder = os.path.join('outputs', 'video_to_video_outputs')
    os.makedirs(video_folder, exist_ok=True)
    video_path = os.path.join(video_folder, file.filename)
    file.save(video_path)

    # Conversión del video
    converter = VideoConverter(video_path)
    converter.to_format(
        output_format=output_format,
        fps=fps,
        video_codec=vcodec,
        audio_codec=acodec,
        audio_channels=audio_channels
    )

    filename = os.path.splitext(os.path.basename(video_path))[0]
    video_path_converted = os.path.join('outputs', 'video_to_video_outputs', f"{filename}.{output_format}")

    if (video_path != video_path_converted):
        os.remove(video_path)

    download_url = request.host_url + '/api/download-video/' + filename + '.' + format

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
        image_path = save_file(request, 'image', 'image_converted_outputs', VALID_IMAGE_EXTENSIONS)
    except ValueError as e:
        return jsonify({"error": e.args[0]}), 400

    try:
        converter = ImageConverter(image_path)
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
        output_path = converter.convert(resize=resize_measures, resize_type=resize_type, format=format, 
                                        angle=rotate_angle, grayscale=grayscale, filters=filters)
    except ValueError as e:
        return jsonify({"message": e}), 400

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

    os.remove(audio_path)

    if converted_audio_path:
        return jsonify({"message": "Conversión exitosa.",
                        "converted_audio_path": '/' + converted_audio_path.replace("\\", "/")
                        }), 200
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

    file_path = os.path.join('outputs', dir, file.filename)
    file.save(file_path)

    return file_path


# search file in db, saves file if it does not exist, returns a tuple (file_in_db, file_path) where:
# file_in_db is a boolean that indicates if the files already exists in db or not
# if the file exists file_path is the path to the frames, otherwise points to the video renamed with its checksum
def get_or_save(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

    try:
        checksum= generate_checksum(file_path)
    except Exception as e:
        raise IOError(f"Se produjo un error al generar el checksum del archivo {file_path}: {str(e)}")

    existing_file = File.query.filter_by(checksum=checksum).first()
    if existing_file:
        return True,existing_file.output_path

    file_extension= file_path.split('.')[-1]
    new_file = File(file_extension=file_extension,checksum=checksum)

    original_folder = os.path.dirname(file_path)
    new_path = os.path.join(original_folder, new_file.checksum+'.'+new_file.file_extension)
    os.rename(file_path,new_path) # rename file to its checksum

    new_file.output_path=os.path.join(original_folder, new_file.checksum)
    new_file.file_path = new_path # updates the file object to save in db

    try:
        db.session.add(new_file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ConnectionError(f"Se produjo un error al guardar el archivo en  Base de Datos: {str(e)}")
    return False,new_path


def generate_checksum(filename):
    h  = hashlib.sha256()
    b  = bytearray(2**18)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()



