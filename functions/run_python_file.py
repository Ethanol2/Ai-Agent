import os;
import subprocess;
from functions.is_inside_dir import is_inside_dir;
from google.genai import types;

def run_python_file(working_directory, file_path):

    if (not is_inside_dir(working_directory, file_path, True)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    combined_path = os.path.join(working_directory, file_path)

    if (not os.path.exists(combined_path)):
        return f'Error: File "{file_path}" not found.'
    
    if (not ".py" in os.path.basename(file_path)):
        return f'Error: "{file_path}" is not a Python file.'
    
    result = None
    try:
        result = subprocess.run(["python3", combined_path], timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"    

    output = []
    if (result != None):
        output.append(f"STDOUT: {result.stdout}")
        output.append(f"STDERR: {result.stderr}")

        err_code = result.returncode
        if (err_code != 0):
            output.append(f"Process exited with code {err_code}")
    else:
        output.append("No output produced")
    
    return tuple(output)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the file in file_path using python3. Assuming the file exists, is within the working directory and has a .py extension",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file. This must be a valid path within the working directory. The file must have a .py extension",
            ),
        },
    ),
)