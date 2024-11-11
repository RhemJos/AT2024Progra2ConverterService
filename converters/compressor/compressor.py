import os
import zipfile


class FolderCompressor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def compress(self):
        parent_dir = os.path.dirname(self.folder_path)  # Obtener el nombre del directorio padre
        zip_filename = os.path.join(parent_dir, os.path.basename(self.folder_path) + '.zip')
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)  # Crea la ruta completa del archivo
                    zipf.write(file_path, os.path.relpath(file_path, self.folder_path))  # Agrega el archivo al zip
        return zip_filename
