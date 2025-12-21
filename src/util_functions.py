import os
import shutil
import re
from markdown_blocks import markdown_to_html_node


def copy_static_to_public():
    # Deleting public folder if it exists
    root_path = os.getcwd()
    if os.path.exists("public"):
        print("Removing public...")
        shutil.rmtree("public")
        print("Public folder removed")
    else:
        print("public doesnt exists")

    files = []  # to be filled with tuples (src_path, dest_path)
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


def extract_title(markdown: str) -> str:
    title_match = re.search(r"^#\s(.*)", markdown, re.MULTILINE)
    if not title_match:
        raise ValueError("This markdown file doesn't have a title")
    return title_match.group(1)


def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise ValueError(f"from_path -> {from_path} does not exist")
    if not os.path.exists(template_path):
        raise ValueError(f"template_path -> {template_path} does not exist")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_content = None
    template_content = None
    with open(from_path) as file:
        from_content = file.read()

    if len(from_content) == 0:
        raise ValueError("Content from source is empty")

    with open(template_path) as templ_file:
        template_content = templ_file.read()

    if len(template_content) == 0:
        raise ValueError("Content from template is empty")

    # use markdown_to_html_node() and .to_html() to convert markdown to html string
    html_node = markdown_to_html_node(from_content)
    html_content = html_node.to_html()

    # extract title from markdown file
    content_title = extract_title(from_content)

    output_file = template_content.replace("{{ Title }}", content_title)
    output_file = output_file.replace("{{ Content }}", html_content)

    # ensure directories exist
    if os.path.dirname(dest_path) != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # write new content to dest_path
    with open(dest_path, "w") as dest_file:
        dest_file.write(output_file)
