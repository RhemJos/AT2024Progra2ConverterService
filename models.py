#
# @models.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import uuid
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checksum = db.Column(db.String(64), nullable=False,unique=True)
    file_extension = db.Column(db.String(10), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    output_path = db.Column(db.String(200))

