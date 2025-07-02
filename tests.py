from functions.get_files_info import get_files_info;
from functions.get_file_content import get_file_content;

def test_list_dir(working_dir, dir):
    print("\n-----------------------------")
    print(f"Working Director: {working_dir}\nDirectory: {dir}\n");
    print(get_files_info(working_dir, dir))
    print("\n-----------------------------")

def test_get_file(working_dir, path):
    print("\n-----------------------------")
    print(f"Working Director: {working_dir}\nFile: {path}\n");
    print(get_file_content(working_dir, path))
    print("\n-----------------------------")

# Test List Directory
if False:
    test_list_dir("calculator", ".")
    test_list_dir("calculator", "pkg")
    test_list_dir("calculator", "/bin")
    test_list_dir("calculator", "../")

# Test Get File
elif True:
    #test_get_file("calculator", "lorem.txt")
    test_get_file("calculator", "main.py")
    test_get_file("calculator", "pkg/calculator.py")
    test_get_file("calculator", "/bin/cat")
