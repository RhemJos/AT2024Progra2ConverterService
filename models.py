import os
import uuid

from flask_sqlalchemy import SQLAlchemy
import hashlib


db = SQLAlchemy()

class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checksum = db.Column(db.String(64), nullable=False,unique=True)
    file_extension = db.Column(db.String(10), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    output_path = db.Column(db.String(200))

