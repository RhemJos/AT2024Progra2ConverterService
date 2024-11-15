import platform
from helpers.utils import CommandExecutor, Formatter
from converters.extractor.extractor import Extractor
import os

class MetadataExtractor(Extractor):
    def extract(self):
        cmd = CommandExecutor() # Ejecutar el comando

        if " " in os.path.basename(self.file_path): #Si el nombre del archivo tiene espacios lo pone entre comillas
            self.file_path = '"' + self.file_path + '"'

        exif_tool_distribution = "exifToolWindows/exiftool.exe" if platform.system() == "Windows" else "exifToolPerl/exiftool" # Determinar el nombre del archivo según el sistema operativo
        exif_tool_path = cmd.get_execfile_path( "converters/extractor/bin/exifTool/" + exif_tool_distribution) #Construir la ruta absoluta del ejecutable exiftool
        exif_tool_command = f"{exif_tool_path} {self.file_path}" #Crear el comando para ejecutar exiftool
        result_text = cmd.run_command(exif_tool_command)
        formatter = Formatter()
        return formatter.key_value_string_to_dict(result_text, ":", "\n")


