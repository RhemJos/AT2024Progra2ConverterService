#
# @compressor.py Copyright (c) 2021 Jalasoft.
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
import zipfile


class FolderCompressor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def compress(self):
        parent_dir = os.path.dirname(self.folder_path)  # Get name of parent directory
        zip_filename = os.path.join(parent_dir, os.path.basename(self.folder_path) + '.zip')
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)  # Create the full path of the file
                    zipf.write(file_path, os.path.relpath(file_path, self.folder_path))  # Add the file to the zip
        return zip_filename
