import re


def extract_markdown_images(text: str):
    re_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return re_images


def extract_markdown_links(text: str):
    re_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return re_links


def extract_title(markdown):
    # pull header from markdown
    # if no header raise exception
    # "# Hello" should return "Hello"
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
        else:
            raise Exception("No title heading found in markdown")
