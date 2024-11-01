import os
from flask import Blueprint, request, jsonify, send_file
from ..converters.video_to_images.video_converter import VideoConverter
from ..converters.image_to_image.image_converter import ImageConverter
from ..converters.audio_to_audio.audio_converter import AudioConverter
from PIL import Image
import mimetypes
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
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    extension = image_file.filename.split('.')[-1].lower()

    if extension not in valid_extensions:
        return jsonify({"error": "Formato de imagen no soportado."}), 400

    image_path = os.path.join('app', 'outputs', 'image_converted_outputs', image_file.filename)
    image_file.save(image_path)

    converter = ImageConverter(image_path, extension)

    # Obtener valores de resize, rotate y grayscale desde el formulario
    resize_width = request.form.get('resize_width', type=int)
    resize_height = request.form.get('resize_height', type=int)
    rotate_angle = request.form.get('rotate', type=int)
    grayscale = request.form.get('grayscale', type=bool)

    output_path = converter.image_convert(resize=(resize_width, resize_height), rotate=rotate_angle, grayscale=grayscale)

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


# Audio Converter - Microservice

@api.route('/convert-audio', methods=['POST'])
def convert_audio():

    if 'audio' not in request.files:
        return jsonify({"error": "No se proporcionó el archivo de audio."}), 400

    audio_file = request.files['audio']
    output_format = request.form.get('output_format', 'mp3')  # Formato predeterminado
    bit_rate = request.form.get('bit_rate')
    channels = request.form.get('channels')
    sample_rate = request.form.get('sample_rate')
    volume = request.form.get('volume')

    audio_path = os.path.join('app', 'outputs', 'audio_converted_outputs', audio_file.filename)
    audio_file.save(audio_path)

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
        return jsonify({"message": "Conversión exitosa.", "converted_audio_path": converted_audio_path.replace("\\", "/")}), 200
    else:
        return jsonify({"error": "Conversión de audio fallida."}), 500