#
# @metadataextractor.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
import platform
from helpers.utils import CommandExecutor, Formatter
from converters.extractor.extractor import Extractor
import os
from exceptions.cmd_execute_exception import CmdExecutionError
from exceptions.metadata_extract_exception import MetadataExtractationError


class MetadataExtractor(Extractor):
    def extract(self):
        cmd = CommandExecutor()  # Execute the command

        if " " in os.path.basename(self.file_path):  # If the file name has spaces, put it in quotes
            self.file_path = '"' + self.file_path + '"'
        # Determine the file name according to the operating system:
        exif_tool_distribution = "exifToolWindows/exiftool.exe" if platform.system() == "Windows" \
            else "exifToolPerl/exiftool"
        # Build the absolute path of the exiftool executable:
        exif_tool_path = cmd.get_execfile_path( "converters/extractor/bin/exifTool/" + exif_tool_distribution)
        exif_tool_command = f"{exif_tool_path} {self.file_path}"  # Create the command to run exiftool
        try:
            result_text = cmd.run_command(exif_tool_command)
        except CmdExecutionError as e:
            raise MetadataExtractationError(f"Exiftool command execution failed: {e.get_message()}", e.get_status_code())
        formatter = Formatter()
        return formatter.key_value_string_to_dict(result_text, ":", "\n")

