import os
import sys
import functions
from dotenv import load_dotenv
from google import genai
from google.genai import types

import functions.get_file_content
import functions.get_files_info
import functions.run_python_file
import functions.write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read a specific file
- Write to a file (it will create the file if missing)
- Run a python file

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def init():
    load_dotenv("gemini_api_key.env")
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    return client


def handle_arguments():
    prompt = ""

    if len(sys.argv) < 2:
        # prompt = input("Prompt: ");
        print("Prompt was expected")
        exit(1)
    else:
        prompt = sys.argv[1]

    if prompt == None or prompt == "":
        print("Empty prompt was provided")
        exit(1)

    args = []

    for i in range(2, len(sys.argv)):
        args.append(sys.argv[i])

    return prompt, args


def print_prompt(prompt, args=[]):
    if "--verbose" in args:
        print(f"\nUser prompt: {prompt}")


def print_response(response: types.GenerateContentResponse, args=[]):

    if response == None:
        return
    if response.text == None or response.usage_metadata == None:
        return

    print(
        "\n===============================================================================\n"
    )

    if "--verbose" in args:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
        print(f"Ai response: {response.text.strip()}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


def handle_function_calls(response: types.GenerateContentResponse, verbose=False):

    if response.function_calls == None:
        return None

    function_calls = []

    if len(response.function_calls) > 0:
        for function_call_part in response.function_calls:

            result = call_function(function_call_part)

            function_call_result = types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=f"{function_call_part.name}",
                        response=result,
                    )
                ],
            )

            if not function_call_result.parts:
                raise Exception(
                    "Something went wrong creating the function result schema"
                )
            else:
                if verbose and not not function_call_result.parts[0].function_response:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

    return function_calls


def call_function(function_call_part: types.FunctionCall, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.args == None:
        function_call_part.args = {}

    function_call_part.args["working_directory"] = "./calculator"

    match function_call_part.name:
        case functions.get_files_info.schema_get_files_info.name:
            return {
                "result": functions.get_files_info.get_files_info(
                    **function_call_part.args
                )
            }

        case functions.get_file_content.schema_get_file_content.name:
            return {
                "result": functions.get_file_content.get_file_content(
                    **function_call_part.args
                )
            }

        case functions.write_file.schema_write_file.name:
            return {
                "result": functions.write_file.write_file(**function_call_part.args)
            }

        case functions.run_python_file.schema_run_python_file.name:
            return {
                "result": functions.run_python_file.run_python_file(
                    **function_call_part.args
                )
            }

        case __:
            return {
                "error": f'Function"{function_call_part.name}" not found. Has it been implemented?'
            }


client = init()
prompt, args = handle_arguments()

available_functions = types.Tool(
    function_declarations=[
        functions.get_files_info.schema_get_files_info,
        functions.get_file_content.schema_get_file_content,
        functions.write_file.schema_write_file,
        functions.run_python_file.schema_run_python_file,
    ]
)

print_prompt(prompt, args)

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

for i in range(0, 20):
    response = client.models.generate_content(
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # if not null
    if not not response.candidates:
        for candidate in response.candidates:
            # if null
            if not candidate.content:
                continue
            messages.append(candidate.content)

    print_response(response, args)
    function_results = handle_function_calls(response, "--verbose" in args)

    if isinstance(function_results, list):
        messages += function_results
    else:
        break
