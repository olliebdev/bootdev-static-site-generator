import re


def extract_markdown_images(text: str):
    re_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return re_images


def extract_markdown_links(text: str):
    re_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return re_links


def extract_title(markdown):
    for line in markdown.split("\n"):
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line[2:]
        raise Exception("No title heading found in markdown")
