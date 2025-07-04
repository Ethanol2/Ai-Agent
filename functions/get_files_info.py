import os;
from functions.is_inside_dir import is_inside_dir;
from google.genai import types;

def get_files_info(working_directory, directory = None):

    combined_path = ""

    if (directory == "." or directory is None):
        combined_path = working_directory + "/"
    elif (".." in directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        combined_path = os.path.join(working_directory, directory)
        
        if (not is_inside_dir(working_directory, directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if (not os.path.isdir(combined_path)):
            return f'Error: "{directory}" is not a directory'
    
    try:
        dir_contents = os.listdir(combined_path);

        if (len(dir_contents) > 10):
            return "Erorr: There are WAY too many files in here. Something went wrong"

        output = "";
        for item in dir_contents:
            item_path = os.path.join(combined_path, item);
            output += f"- {item}: ";
            output += f"file_size={os.path.getsize(item_path)}, ";
            output += f"is_dir={os.path.isdir(item_path)}\n"
    except Exception as e:
        return f"Error: {e}\nTraceback: {e.with_traceback}"


    return output.strip();

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)