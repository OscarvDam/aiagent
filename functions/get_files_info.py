import os

def get_files_info(working_directory, directory="."):
    try:
        directory_path = os.path.join(working_directory, directory)
        abs_working_directory = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(directory_path)
        if not abs_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'
        directory_list = os.listdir(directory_path)
        string_response = []
        for directory_item in directory_list:
            abs_directory_item = abs_directory + "/" + directory_item
            file_size = os.path.getsize(abs_directory_item)
            is_dir = os.path.isdir(abs_directory_item)
            new_string = f"- {directory_item}: file_size={file_size}, is_dir={is_dir}"
            string_response.append(new_string)
        response = "\n".join(string_response)
        return response
    except Exception as e:
        print(f"Error encountered: {e}")

def main():
    print(get_files_info("calculator", "pkg"))

if __name__ == "__main__":
    main()
