import os

from flask_sqlalchemy import SQLAlchemy
import hashlib


db = SQLAlchemy()

# class FilePath(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     path = db.Column(db.String(255), nullable=False)

class Converter(db.Model):
    __tablename__ = 'converter'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    checksum = db.Column(db.String(100), nullable=False,unique=True)

    # def generate_checksum(self):
    #     hash_md5 = hashlib.md5()
    #     with open(self.file_path, "rb") as f:
    #         while chunk := f.read(4096):
    #             hash_md5.update(chunk)
    #     self.checksum = hash_md5.hexdigest()
    def generate_checksum(self,file_content):
        self.checksum = hashlib.sha256(file_content).hexdigest()
