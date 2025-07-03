import os;
from functions.is_inside_dir import is_inside_dir;

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