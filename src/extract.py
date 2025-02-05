import re


def extract_markdown_images(text: str):
    re_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return re_images


def extract_markdown_links(text: str):
    re_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return re_links
