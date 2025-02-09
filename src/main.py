import os
import shutil
from page_gen import generate_page, generate_pages_recursive


def copy_static(src: str, dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        os.mkdir(dest)
    if os.path.exists(src):
        src_files = os.listdir(src)
        for file in src_files:
            if os.path.isfile(os.path.join(src, file)):
                shutil.copy(os.path.join(src, file), os.path.join(dest, file))
            else:
                os.mkdir(os.path.join(dest, file))
                copy_static(os.path.join(src, file), os.path.join(dest, file))


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    src = os.path.join(project_root, "static")
    dest = os.path.join(project_root, "public")
    copy_static(src, dest)

    generate_pages_recursive(
        os.path.join(project_root, "content"),
        os.path.join(project_root, "template.html"),
        os.path.join(project_root, "public"),
    )


main()
