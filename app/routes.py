from flask import Blueprint, request, jsonify, send_file
import os
from .models import db, FilePath 


test_route = Blueprint('test_route', __name__)

@test_route.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        return jsonify({"response": "Hi"})
    elif request.method == "POST":
        req_Json = request.json
        name = req_Json["name"]
        return jsonify({"response": "Hi " + name})



@test_route.route('/upload-file', methods=['POST'])
def upload_file():
    upload_folder = os.path.join('app', 'uploads')

    if 'file' not in request.files:
        return jsonify({"response": "No se ha enviado ningun 'file' en la solicitud."})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"response": "No se ha seleccionado ningún archivo."})

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)

    existing_file = FilePath.query.filter_by(path=file_path).first()
    if existing_file:
        return jsonify({"response": "El archivo ya existe en la base de datos."})

    file.save(file_path)

    new_file_path = FilePath(path=file_path)
    db.session.add(new_file_path)
    db.session.commit()

    return jsonify({"response": "El archivo se ha almacenado en la base de datos."})



@test_route.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(current_dir, 'uploads')
    file_path = os.path.join(upload_folder, filename)

    if os.path.isfile(file_path):
        try:
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": "Error al descargar el archivo", "details": str(e)})
    else:
        return jsonify({"error": "El archivo no existe en el directorio."})



@test_route.route('/get-file', methods=['GET'])
def get_file():
    file_path = "C:/white-rinon.png"
    
    if os.path.isfile(file_path):
        try:
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"response": "El archivo no existe en el directorio."})