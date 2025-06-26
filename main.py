import os;
import sys;
from dotenv import load_dotenv;
from google import genai;
from google.genai import types;

def init():
    load_dotenv("gemini_api_key.env");
    api_key = os.environ.get("GEMINI_API_KEY");

    client = genai.Client(api_key=api_key);
    return client;

def handle_arguments():
    prompt = "";

    if (len(sys.argv) < 2):
        # prompt = input("Prompt: ");
        print("Prompt was expected")
        exit(1);
    else:
        prompt = sys.argv[1];
    
    if (prompt == None or prompt == ""):
        print("Empty prompt was provided")
        exit(1);
    
    args = []

    for i in range(2, len(sys.argv)):
        args.append(sys.argv[i])    

    return prompt, args;

def print_prompt(prompt, args = []):
    if ("--verbose" in args):
        print(f"\nUser prompt: {prompt}")

def print_response(response, args = []):
    if ("--verbose" in args):
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")  
        print(f"Ai response: {response.text.strip()}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)

client = init();
prompt, args = handle_arguments();

print_prompt(prompt, args)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]

response = client.models.generate_content(
    model = "gemini-2.0-flash-001", 
    contents = messages);

print_response(response, args)