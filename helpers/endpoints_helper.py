import os
import hashlib
from models import db, File


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

# method to save file on DB, changing its name to its checksum
def save_db(file_path, checksum=None):
    if not checksum:
        try:
            checksum = generate_checksum(file_path)
        except Exception as e:
            raise IOError(f"Se produjo un error al generar el checksum del archivo {file_path}: {str(e)}")

    file_extension = file_path.split('.')[-1]
    file = File(file_extension=file_extension, checksum=checksum)

    original_folder = os.path.dirname(file_path)
    new_path = os.path.join(original_folder, file.checksum + '.' + file.file_extension)
    os.rename(file_path, new_path)  # rename file to its checksum

    file.file_path = new_path  # updates the file object to save in db

    try:
        db.session.add(file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ConnectionError(f"Se produjo un error al guardar el archivo en  Base de Datos: {str(e)}")
    return File.query.filter_by(checksum=file.checksum).first()


# search file in db, saves file if it does not exist, returns a tuple (file_in_db, file) where:
# file_in_db is a boolean that indicates if the file already exists in db or not
# file is the object File from DB
def get_or_save(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

    try:
        checksum= generate_checksum(file_path)
    except Exception as e:
        raise IOError(f"Se produjo un error al generar el checksum del archivo {file_path}: {str(e)}")

    existing_file = File.query.filter_by(checksum=checksum).first()
    if existing_file:
        os.remove(file_path)
        return True,existing_file
    else:
        return False,save_db(file_path, checksum)


def update(file):
    try:
        db.session.add(file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ConnectionError(f"Se produjo un error al actualizar el archivo en  Base de Datos: {str(e)}")




def generate_checksum(filename):
    h  = hashlib.sha256()
    b  = bytearray(2**18)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()