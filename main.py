import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import *
from call_functions import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")
    client = genai.Client(api_key=api_key)


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages, 
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )
    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, args.verbose)
        if result.parts == []:
            raise RuntimeError
        if result.parts[0].function_response is None:
            raise RuntimeError
        if result.parts[0].function_response.response is None:
            raise RuntimeError
        if args.verbose:
            # Extract the dictionary
            response_dict = result.parts[0].function_response.response
            # Get the "result" string, defaulting to an empty string if it's missing
            result_text = response_dict.get("result", "")
            print(f"-> Result:\n{result_text}")


    '''if response.usage_metadata is not None and args.verbose is True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")'''
    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")
    
if __name__ == "__main__":
    main()


