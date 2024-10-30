import platform
from utils import CommandExecutor
from extractor import Extractor


class MetadataExtractor(Extractor):
    def extract(self):
        exif_tool_distribution = "Windows" if platform.system() == "Windows" else "Perl" 
        cmd = CommandExecutor()
        exif_tool_path = cmd.get_execfile_path("\\bin\\exifTool\\exifTool{}".format(exif_tool_distribution) )
        exif_tool_command = "{}\\exiftool {}".format(exif_tool_path, self.file_path) 
        return cmd.run_command(exif_tool_command)

