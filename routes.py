from flask import Blueprint, request, jsonify, send_file
import os
from models import db, Converter


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
    file_content = file.read()

    new_file = Converter(file_path=file_path,file_name=file.filename)
    new_file.generate_checksum(file_content)

    existing_file = Converter.query.filter_by(checksum=new_file.checksum).first()
    if existing_file:
        return jsonify({"response": "El archivo ya existe en la base de datos."})

    try:
        db.session.add(new_file)
        db.session.commit()
    except Exception:
        return jsonify({"response": "Error al guardar el archivo en base de datos."})
    else:
        # file.save(file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(file_content)

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