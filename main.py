import sys
import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
user_prompt = sys.argv[1]

dictionary_function_call = {

        }

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) == 1:
        print("no prompt given")
        exit(1)
    for i in range(20):
        # Add a small delay between requests
        if i > 0:
            time.sleep(4)  # Wait 4 seconds between requests
        response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
        )
        try:
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
        except Exception as e:
            print(f"No candidate found {e}")


        if response.function_calls:
            # Collect ALL function call responses first
            function_response_parts = []

            for function_call_part in response.function_calls:
                if "--verbose" in sys.argv:
                    result_function_call = call_function(function_call_part, verbose=True)
                else:
                    result_function_call = call_function(function_call_part)

                if not result_function_call.parts:
                    raise Exception("Error: no parts found to the function call")
                if not result_function_call.parts[0].function_response:
                    raise Exception("Error: no response found")
                if not result_function_call.parts[0].function_response.response:
                    raise Exception("Error: no results found")

                # Add the function response part to our collection
                function_response_parts.extend(result_function_call.parts)

            # Now send ALL function responses in a single message
            messages.append(types.Content(role="tool", parts=function_response_parts))
            continue

        if response.text:
            print(response.text)
            if response.usage_metadata:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
            else:
                print("No usage metadata available")
            break
        
        if response.usage_metadata:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        else:
            print("No usage metadata available")


def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info("./calculator", **function_call_part.args)
        case "get_file_content":
            function_result = get_file_content("./calculator", **function_call_part.args)
        case "write_file":
            function_result = write_file("./calculator", **function_call_part.args)
        case "run_python_file":
            function_result = run_python_file("./calculator", **function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
    )
        

if __name__ == "__main__":
    main()
