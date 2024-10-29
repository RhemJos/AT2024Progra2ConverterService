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

@test_route.route('/path', methods=['POST'])
def find_path():
    req_json = request.json
    file_path = req_json.get("file_path")

    if os.path.isfile(file_path):
        new_file_path = FilePath(path=file_path)
        db.session.add(new_file_path)
        db.session.commit()
        return jsonify({"response": "El archivo existe y se ha almacenado en la base de datos."})
    else:
        return jsonify({"response": "El archivo no existe en el directorio."})

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
