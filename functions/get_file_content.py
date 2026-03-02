import os 
from config import *
def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS) 
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{target_file}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e: 
        return f'Error: {e}'
