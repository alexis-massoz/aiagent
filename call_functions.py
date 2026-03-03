from google import genai
from functions.get_files_info import schema_get_files_info

available_functions = genai.types.Tool(
    function_declarations=[schema_get_files_info],
)