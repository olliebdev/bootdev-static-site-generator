from blocks import markdown_to_html_node
from htmlnode import HTMLNode
from extract import extract_title
import os


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown_file = file.read()
    with open(template_path, "r") as file:
        template_file = file.read()

    title = str(extract_title(markdown_file))
    markdown_html = markdown_to_html_node(markdown_file).to_html()

    template_file = template_file.replace("{{ Title }}", title).replace(
        "{{ Content }}", markdown_html
    )

    dest_directory = os.path.dirname(dest_path)
    if dest_directory:
        os.makedirs(dest_directory, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_files = os.listdir(dir_path_content)
    for file in content_files:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file.replace(".md", ".html")),
            )
        else:
            os.makedirs(os.path.join(dest_dir_path, file), exist_ok=True)
            generate_pages_recursive(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file),
            )
