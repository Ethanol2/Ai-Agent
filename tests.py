import sys;
import os;
from functions.get_files_info import get_files_info;
from functions.get_file_content import get_file_content;
from functions.write_file import write_file;
from functions.run_python_file import run_python_file;

def print_header(text):
    print(f"\n===== {text} =====")

def test_list_dir(working_dir, dir):
    print("\n-----------------------------")
    print(f"Working Directory: {working_dir}\nDirectory: {dir}\n");
    print(get_files_info(working_dir, dir))
    print("\n-----------------------------")

def test_get_file(working_dir, path):
    print("\n-----------------------------")
    print(f"Working Directory: {working_dir}\nFile: {path}\n");
    print(get_file_content(working_dir, path))
    print("\n-----------------------------")

def test_write_file(working_dir, path, content, delete_file = False):
    print("\n-----------------------------")
    print(f"Working Directory: {working_dir}\nFile: {path}\nDelete File: {delete_file}\n");
    
    if (delete_file and os.path.exists(os.path.join(working_dir, path))):
        os.remove(os.path.join(working_dir, path))

    print(write_file(working_dir, path, content))
    print("\n-----------------------------")

def test_run_python_file(working_dir, path):
    print("\n-----------------------------")
    print(f"Working Directory: {working_dir}\nFile: {path}\n");
    print(run_python_file(working_dir, path))
    print("\n-----------------------------")

def main(default_test = "-p"):
    if (len(sys.argv) < 2):
        print("No tests specified" \
        "\n\t-l : Run get_files_info tests" \
        "\n\t-r : Run get_file_content tests" \
        "\n\t-w : Run write_file tests" \
        "\n\t-p : Run run_python_file tests" \
        "\n\nRunning Default Test")
        
        sys.argv.append(default_test)

    # Test List Directory
    if "-l" in sys.argv:
        print_header("get_file_info tests")
        test_list_dir("calculator", ".")
        test_list_dir("calculator", "pkg")
        test_list_dir("calculator", "/bin")
        test_list_dir("calculator", "../")

    # Test Get File
    if "-r" in sys.argv:
        print_header("get_file_content tests")
        #test_get_file("calculator", "lorem.txt")
        test_get_file("calculator", "main.py")
        test_get_file("calculator", "pkg/calculator.py")
        test_get_file("calculator", "/bin/cat")

    # Test Write to File
    if "-w" in sys.argv:
        print_header("write_file tests")
        test_write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        test_write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", True)
        test_write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    
    if "-p" in sys.argv:
        print_header("run_python_file tests")
        test_run_python_file(".", "pytest.py")
        test_run_python_file("calculator", "main.py")
        test_run_python_file("calculator", "tests.py")
        test_run_python_file("calculator", "../main.py")
        test_run_python_file("calculator", "nonexistent.py")


main();