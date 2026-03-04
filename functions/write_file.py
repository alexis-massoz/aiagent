import os 
from google import genai

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes in a specified file relative to the working directory",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Directory path to file from, relative to the working directory (default is the working directory itself)",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="content to write in file",
            ),
        },
        required=["file_path", "content"]
    ),
    
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(file_path, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e: 
        return f'Error: {e}'
