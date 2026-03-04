import os 
import subprocess
from google import genai

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file relative to the working directory",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Directory path to python file from, relative to the working directory (default is the working directory itself)",
            ),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                description="optionnal array of string arguments for running python files",
                items= genai.types.Schema(
                    type=genai.types.Type.STRING
                )
            ),
        },
        required=["file_path"]
    ),
    
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        complete_process_object = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_list = []
        if complete_process_object.returncode !=0:
            output_list.append(f'Process exited with code {complete_process_object.returncode}')
        if complete_process_object.stdout == "":
            output_list.append('No output produced')
        else :
            output_list.append(f'STDOUT: {complete_process_object.stdout}') 
        if complete_process_object.stderr == "":
            output_list.append('No output produced')
        else:
            output_list.append(f'STDERR: {complete_process_object.stderr}')
        return "\n".join(output_list)
    except Exception as e: 
        return f"Error: executing Python file: {e}"