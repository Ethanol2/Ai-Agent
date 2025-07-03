import os;

def is_inside_dir(start_dir, path, ignore_file = False):
    if (ignore_file):
        dir_path = os.path.dirname(path);

        if (dir_path == '' or dir_path == '.'):
            return True;

        path = dir_path;

    return __is_inside_dir(start_dir, path.split("/"))

def __is_inside_dir(start_dir, split_path):
    if (len(split_path) < 1):
        return True;

    for item in os.listdir(start_dir):
        if (item == split_path[0]):
            return __is_inside_dir(os.path.join(start_dir, item), split_path[1:]);
    
    return False;
