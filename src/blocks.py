from split import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
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
    div_block = ParentNode("div", [])
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            split_block = block.split(" ", 1)
            heading_level = split_block[0].count("#")
            text = split_block[1]
            heading_node = ParentNode(f"h{heading_level}", text_to_children(text))
            div_block.children.append(heading_node)

        elif block_type == "paragraph":
            paragraph_node = ParentNode("p", text_to_children(block))
            div_block.children.append(paragraph_node)

        elif block_type == "unordered_list":
            ul_node = ParentNode("ul", [])
            block_lines = block.split("\n")
            for line in block_lines:
                line = line.strip()
                if line.startswith("* ") or line.startswith("- "):
                    block_text = line[2:].strip()
                    li_node = ParentNode("li", text_to_children(block_text))
                elif line == "*" or line == "-":
                    li_node = ParentNode("li", [])
                else:
                    continue
                ul_node.children.append(li_node)
            div_block.children.append(ul_node)

        elif block_type == "ordered_list":
            ol_node = ParentNode("ol", [])
            block_lines = block.split("\n")
            for line in block_lines:
                line = line.strip()
                index = line.find(" ")
                block_text = line[index + 1 :].strip()
                li_node = ParentNode("li", text_to_children(block_text))
                ol_node.children.append(li_node)
            div_block.children.append(ol_node)

        elif block_type == "quote":
            lines = block.split("\n")
            cleaned_lines = [line.strip().removeprefix(">").strip() for line in lines]
            quote_text = "\n".join(cleaned_lines)
            quote_node = ParentNode("blockquote", text_to_children(quote_text))
            div_block.children.append(quote_node)

        elif block_type == "code":
            code_text = block[3:-3].strip()
            if code_text.strip() == "":
                code_text = "\n"
            else:
                code_text = code_text.rstrip()
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            pre_node = ParentNode("pre", [code_node])
            div_block.children.append(pre_node)
    return div_block
