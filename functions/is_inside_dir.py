import os;

def is_inside_dir(start_dir, path):
    return is_inside_dir(start_dir, path.split("/"))

def is_inside_dir(start_dir, split_path):
    if (len(split_path) < 1):
        return True;

    for item in os.listdir(start_dir):
        if (item == split_path[0]):
            return is_inside_dir(os.path.join(start_dir, item), split_path[1:]);
    
    return False;
