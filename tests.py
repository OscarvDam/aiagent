from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def tests():
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))
    
    print("Results for contents main.py in calculator:")
    print(get_file_content("calculator", "main.py"))
    print("Results for contents calculator.py in calculator/pkg")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("Results for dictonary /bin/cat")
    print(get_file_content("calculator", "/bin/cat"))
    print("Results for non existing file")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

    print("Results for write in lorem.txt:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("Results for write in non-existent file:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("Results for write outside directory:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    print("Result for running the calculator")
    print(run_python_file("calculator", "main.py"))
    print("Result for running calculator with arguments")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("Result for running the tests")
    print(run_python_file("calculator", "tests.py"))
    print("result for running file outside directory")
    print(run_python_file("calculator", "../main.py"))
    print("result for nonexistend python file")
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    tests()
