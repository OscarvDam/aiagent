import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.join(abs_working_directory, file_path)
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        max_chars = 10000

        with open(abs_file_path, "r") as f:
            file_content_string = f.read(max_chars)
        if len(file_content_string) == max_chars:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error encountered: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of files in the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory of the file you want to know content of. It can't be empty",
            ),
        },
    ),
)

def main():
    print(get_file_content("calculator", "pkg/calculator.py"))

if __name__ == "__main__":
    main()
