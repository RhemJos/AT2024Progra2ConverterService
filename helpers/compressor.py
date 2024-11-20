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
    def __init__(self, folder_path):  # The constructor accepts the path of the folder to be compressed
        self.folder_path = folder_path   # Set the folder_path attribute

    def compress(self):  # The method to compress the folder
        parent_dir = os.path.dirname(self.folder_path)  # Get name of parent directory
        # Define the zip file name (same name as the folder, but with a .zip extension)
        zip_filename = os.path.join(parent_dir, os.path.basename(self.folder_path) + '.zip')
        # Create a ZipFile object for writing in "write" mode with deflate compression
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the folder and its subfolders
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)  # Create the full path of the file
        # Add the file to the zip, the second argument ensures the file is stored with the relative path inside the zip
                    zipf.write(file_path, os.path.relpath(file_path, self.folder_path))
        return zip_filename
