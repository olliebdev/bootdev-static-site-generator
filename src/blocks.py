from split import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import HTMLNode
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    current_block = ""
    in_code_block = False

    for line in markdown.split("\n"):
        if line.startswith("```"):
            if not in_code_block:
                if current_block:
                    blocks.append(current_block.strip())
                current_block = line
            else:
                current_block += "\n" + line
                blocks.append(current_block)
                current_block = ""
            in_code_block = not in_code_block
        else:
            if in_code_block:
                current_block += "\n" + line
            else:
                if not line.strip():
                    if current_block:
                        blocks.append(current_block.strip())
                        current_block = ""
                else:
                    if line.startswith("#"):
                        if current_block:
                            blocks.append(current_block.strip())
                            current_block = ""
                        blocks.append(line)
                    else:
                        if current_block:
                            current_block += "\n"
                        current_block += line

    if current_block:
        blocks.append(current_block.strip())

    return [block for block in blocks if block.strip()]


def block_to_block_type(block):
    parts = block.split(" ", 1)
    if len(parts) == 2:
        first_part = parts[0]
        if (
            first_part.count("#") == len(first_part)
            and len(first_part) <= 6
            and len(first_part) > 0
        ):
            return "heading"
    if (
        block.startswith("```")
        and block.endswith("```")
        and not block.startswith("````")
        and not block.endswith("````")
    ):
        return "code"

    if all(line.startswith(">") for line in block.split("\n")):
        return "quote"

    if all(
        line.strip() == "*" or line.strip() == "-" or line.startswith(("* ", "- "))
        for line in block.split("\n")
    ):
        return "unordered_list"
    if all(
        line.strip() == f"{i+1}." or line.startswith(f"{i+1}. ")
        for i, line in enumerate(block.split("\n"))
    ):
        return "ordered_list"

    return "paragraph"


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    div_block = HTMLNode("div")
    div_block.children = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            split_block = block.split(" ", 1)
            heading_level = split_block[0].count("#")
            text = split_block[1]
            heading_node = HTMLNode(f"h{heading_level}")
            heading_node.children = text_to_children(text)
            heading_node.parent = div_block
            div_block.children.append(heading_node)

        elif block_type == "paragraph":
            paragraph_node = HTMLNode("p")
            paragraph_node.children = text_to_children(block)
            paragraph_node.parent = div_block
            div_block.children.append(paragraph_node)

        elif block_type == "unordered_list":
            ul_node = HTMLNode("ul")
            ul_node.children = []
            block_lines = block.split("\n")
            for line in block_lines:
                line = line.strip()
                li_node = HTMLNode("li")
                if line.startswith("* ") or line.startswith("- "):
                    block_text = line[2:].strip()
                    li_node.children = text_to_children(block_text)
                elif line == "*" or line == "-":  # Handle empty list items
                    li_node.children = []
                li_node.parent = ul_node
                ul_node.children.append(li_node)
            ul_node.parent = div_block
            div_block.children.append(ul_node)

        elif block_type == "ordered_list":
            ol_node = HTMLNode("ol")
            ol_node.children = []
            block_lines = block.split("\n")
            for line in block_lines:
                line = line.strip()
                index = line.find(" ")
                block_text = line[index + 2 :].strip()
                li_node = HTMLNode("li")
                li_node.children = text_to_children(block_text)
                li_node.parent = ol_node
                ol_node.children.append(li_node)
            ol_node.parent = div_block

            div_block.children.append(ol_node)
        elif block_type == "quote":
            quote_node = HTMLNode("blockquote")
            lines = block.split("\n")
            cleaned_lines = [line.strip().removeprefix(">").strip() for line in lines]
            quote_text = "\n".join(cleaned_lines)
            quote_node.children = text_to_children(quote_text)
            quote_node.parent = div_block
            div_block.children.append(quote_node)

        elif block_type == "code":
            code_text = block[3:-3]
            if code_text.strip() == "":
                code_text = "\n"
            else:
                code_text = code_text.rstrip()
            pre_node = HTMLNode("pre")
            code_node = HTMLNode("code")
            code_node.children = [
                text_node_to_html_node(TextNode(code_text, TextType.CODE))
            ]
            code_node.parent = pre_node
            pre_node.children = [code_node]
            pre_node.parent = div_block
            div_block.children.append(pre_node)
    return div_block
