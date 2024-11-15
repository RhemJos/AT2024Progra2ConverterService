#
# @endpoints_helper.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import os
import hashlib
from models import db, File
from flask import jsonify, send_file


# Extracts file from request, check its extension(optional) and saves it in the corresponding directory
def save_file(request, file_type, directory, valid_formats=None):
    if file_type not in request.files:
        raise ValueError(f"No {file_type} has been submitted in the request.")

    file = request.files[file_type]
    if file.filename == '':
        raise ValueError("No file has been selected.")

    if valid_formats:
        extension = file.filename.split('.')[-1].lower()
        if extension not in valid_formats:
            raise ValueError(f"{file_type} format not supported.")

    file_folder = os.path.join('outputs', directory)
    os.makedirs(file_folder, exist_ok=True)

    file_path = os.path.join('outputs', directory, file.filename)
    file.save(file_path)

    return file_path


# Save file on DB, rename with its checksum
def save_db(file_path, checksum=None):
    if not checksum:
        try:
            checksum = generate_checksum(file_path)
        except Exception as e:
            raise IOError(f"An error occured while generating file checksum of {file_path}: {str(e)}")

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
        raise ConnectionError(f"An error occurred while saving the file to the Database: {str(e)}")
    return File.query.filter_by(checksum=file.checksum).first()


# search file in db, save file if it does not exist, returns a tuple (file_in_db, file) where:
# file_in_db is a boolean that indicates if the file already exists in db or not
# file is the object File from DB
def get_or_save(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} doesn't exist.")

    try:
        checksum= generate_checksum(file_path)
    except Exception as e:
        raise IOError(f"An error occured while generating file checksum of {file_path}: {str(e)}")

    existing_file = File.query.filter_by(checksum=checksum).first()
    if existing_file:
        os.remove(file_path)
        return True, existing_file
    else:
        return False, save_db(file_path, checksum)


def update(file):
    try:
        db.session.add(file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ConnectionError(f"An error occurred while updating the file in Database: {str(e)}")


def generate_checksum(filename):
    h = hashlib.sha256()
    b = bytearray(2**18)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()


def send_file_download(folder, file_name, type_file="File"):
    try:
        file_path = os.path.join('outputs', folder, file_name)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=file_name)
        else:
            return jsonify({"error": f"{type_file} not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
