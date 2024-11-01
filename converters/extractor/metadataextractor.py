import platform
import os
from utils import CommandExecutor, Formatter
from converters.extractor.extractor import Extractor

class MetadataExtractor(Extractor):
    def extract(self):
        
        exif_tool_distribution = "exifTool/exifToolWindows/exiftool.exe" if platform.system() == "Windows" else "exifToolPerl/exiftool" # Determinar el nombre del archivo según el sistema operativo
        base_dir = os.path.dirname(os.path.abspath(__file__))# Obtener la ruta base del archivo actual
        exif_tool_path = os.path.join(base_dir, "bin", exif_tool_distribution).replace("\\", "/") #Construir la ruta absoluta del ejecutable exiftool
        
        if not os.path.isfile(exif_tool_path):
            return {"error": f"No se encontró el archivo exiftool en la ruta: {exif_tool_path}"}
        
        exif_tool_command = f"{exif_tool_path} {self.file_path}" #Crear el comando para ejecutar exiftool
        
        cmd = CommandExecutor() # Ejecutar el comando
        result_text = cmd.run_command(exif_tool_command)
        
        formatter = Formatter() # Formatear el resultado a diccionario
        return formatter.key_value_string_to_dict(result_text, ":", "\n")

