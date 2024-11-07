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

    def generate_checksum(self):
        self.checksum= hashlib.md5(self.file_name.encode()).hexdigest()