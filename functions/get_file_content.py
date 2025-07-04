import os;
from functions.is_inside_dir import is_inside_dir;
from google.genai import types;

def get_file_content(working_directory, file_path):
    
    if (not is_inside_dir(working_directory, file_path)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    combined_path = os.path.join(working_directory, file_path)
    
    if (not os.path.isfile(combined_path)):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        MAX_CHARS = 10000;
        with open(combined_path, "r") as f:
            file_contents = f.read(MAX_CHARS);

        if (len(file_contents) == MAX_CHARS):
            file_contents += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {e}\nTraceback: {e.with_traceback}"
    
    return file_contents;

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file, with a max char limit of 10000. Assuming the file exists and is within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file. This must be a valid path within the working directory",
            ),
        },
    ),
)