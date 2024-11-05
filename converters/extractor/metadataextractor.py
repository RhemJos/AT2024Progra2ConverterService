import platform
from utils import CommandExecutor, Formatter
from converters.extractor.extractor import Extractor


class MetadataExtractor(Extractor):
    def extract(self):
        exif_tool_distribution = "Windows" if platform.system() == "Windows" else "Perl" 
        cmd = CommandExecutor()
        exif_tool_path = cmd.get_execfile_path("\\converters\\extractor\\bin\\exifTool\\exifTool{}".format(exif_tool_distribution) )
        exif_tool_command = "{}\\exiftool {}".format(exif_tool_path, self.file_path) 
        result_text = cmd.run_command(exif_tool_command)
        formatter = Formatter()
        return formatter.key_value_string_to_dict(result_text, ":", "\n")


