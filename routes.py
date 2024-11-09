from flask import Blueprint, request, jsonify, send_file
import os
from models import db, File


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
    file.save(file_path)

    file_in_db, new_path = get_or_save(file_path)

    if file_in_db:
        os.remove(file_path)
        return jsonify({"message": "Video ya existe.", "output_path": '/' + new_path.replace("\\", "/")})

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


# search file in db, saves file if it does not exist, returns a tuple (file_in_db, file_path) where:
# file_in_db is a boolean that indicates if the files already exists in db or not
# if the file exists file_path is the path to the frames, otherwise points to the video renamed with its checksum
def get_or_save(file_path):
    checksum= generate_checksum(file_path)
    existing_file = File.query.filter_by(checksum=checksum).first()
    if existing_file:
        return True,existing_file.output_path

    file_extension= file_path.split('.')[-1]
    new_file = File(file_extension=file_extension,checksum=checksum)

    new_path = os.path.join(os.path.dirname(file_path), new_file.checksum+'.'+new_file.file_extension)
    os.rename(file_path,new_path) # rename file to its checksum

    new_file.output_path=os.path.join('outputs','video_to_frames_output', new_file.checksum)
    new_file.file_path = new_path # updates the file object to save in db

    db.session.add(new_file)
    db.session.commit()

    return False,new_path

def generate_checksum(filename):
    h  = hashlib.sha256()
    b  = bytearray(2**18)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()