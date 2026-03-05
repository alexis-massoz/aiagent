import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import *
from call_functions import *
import sys

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

    for _ in range(20):
    # call the model, handle responses, etc.
        result = generate_content(client, messages, args.verbose)
        if result is not None:
            print("Final response:")
            print(result)
            return 
        
    print('Max iteration reached with no response')
    sys.exit(1)

    

def generate_content(client, messages, verbose):    
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages, 
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )

    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            # each candidate has a .content property
            #print(candidate.content)
            messages.append(candidate.content)

   
    if not response.function_calls:
        return response.text
        

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if result.parts == []:
            raise RuntimeError
        if result.parts[0].function_response is None:
            raise RuntimeError
        if result.parts[0].function_response.response is None:
            raise RuntimeError
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
    messages.append(types.Content(role="user", parts=function_responses))
    return None   
        #if verbose:
            # Extract the dictionary
           # response_dict = result.parts[0].function_response.response
            # Get the "result" string, defaulting to an empty string if it's missing
          #  result_text = response_dict.get("result", "")
           # print(f"-> Result:\n{result_text}")
          #  messages.append(types.Content(role="user", parts=function_responses))

    
if __name__ == "__main__":
    main()


