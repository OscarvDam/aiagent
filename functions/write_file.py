import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.join(abs_working_directory, file_path)
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error encountered: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite the specified file with new content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory of the file you want to write or override",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which that will be written or override the file with",
            )
        },
    ),
)

def main():
    write_file("calculator", "lorem.txt", "test")

if __name__ == "__main__":
    main()
