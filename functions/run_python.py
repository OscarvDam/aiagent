import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path_encode = os.path.join(abs_working_directory, file_path)
        abs_file_path = os.path.abspath(abs_file_path_encode)
        if not abs_file_path.startswith(abs_working_directory):
            return  f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'       
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.split(".")[-1] == "py":
           return f'Error: "{file_path}" is not a Python file.'
        result = subprocess.run([sys.executable, file_path], timeout=30, capture_output=True, cwd=abs_working_directory)
        output = ""
        if result.stdout.decode("utf-8") != "":
            output += "STDOUT:\n" + result.stdout.decode("utf-8")
        if result.stderr.decode("utf-8") != "":
            output += "STDERR:\n" + result.stderr.decode("utf-8")
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        if output == "":
            output += "No output produced"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the given filepath, with additional arguments if needed. Bound to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to run. And returns an error if not a python file",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="A list of optional arguments, this list is optional. If no arguments are given you can remove this from the output",
            ),
        },
    ),
)

def main():
    print(run_python_file("calculator", "main.py"))

if __name__ == "__main__":
    main()
