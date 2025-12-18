import os
import shutil


def copy_static_to_public():
    # Deleting public folder if it exists
    root_path = os.getcwd()
    if os.path.exists("public"):
        print("Removing public...")
        shutil.rmtree("public")
        print("Public folder removed")
    else:
        print("public doesnt exists")

    files = []
    directories = ["static"]
    dirs_to_create = []

    # recursively explore folders and files
    while len(directories) > 0:
        curr_dir = directories.pop()
        dir_to_create = replace_static_to_public_paths(curr_dir)
        dirs_to_create.append(dir_to_create)
        files_in_curr_dir = os.listdir(curr_dir)
        for path in files_in_curr_dir:
            path = os.path.join(curr_dir, path)
            if os.path.isfile(path):
                file_to_create = replace_static_to_public_paths(path)
                files.append((path, file_to_create))
            else:
                directories.append(path)

    # create all directories
    for dir_path in dirs_to_create:
        if not os.path.exists(dir_path):
            print("Creating directory: ", dir_path)
            os.mkdir(dir_path)

    # copy all files
    for src_file, dest_file in files:
        print(f"Copying file from {src_file} -> {dest_file}")
        shutil.copy(src_file, dest_file)


def replace_static_to_public_paths(path: str):
    if path == "static":
        return "public"
    elif path.startswith("static/"):
        return path.replace("static/", "public/", 1)
