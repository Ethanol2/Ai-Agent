import os;
from functions.is_inside_dir import is_inside_dir;
from google.genai import types;

def write_file(working_directory, file_path, content):

    if (not is_inside_dir(working_directory, file_path, True)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory';

    combined_path = os.path.join(working_directory, file_path)

    try:
        with open(combined_path, "w") as f:
            f.write(content);
    except Exception as e:
        return f"Error: {e}\nTraceback: {e.with_traceback}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes contents to a file. Assuming the directory is within the working directory, the contents will overwrite the existing file, or create a new one.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file. This must be a path within the working directory. Will create a file if it doesn't exist",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file"
            )
        },
    ),
)