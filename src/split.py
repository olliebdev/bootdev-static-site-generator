import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        if delimiter not in remaining_text:
            if remaining_text != "":
                new_nodes.append(node)
            continue
        while delimiter in remaining_text:
            first_delim = remaining_text.find(delimiter)
            second_delim = remaining_text.find(delimiter, first_delim + 1)
            if second_delim == -1:
                text_with_delim = remaining_text[: first_delim + len(delimiter)]
                new_nodes.append(TextNode(text_with_delim, TextType.TEXT))
                remaining_text = remaining_text[first_delim + len(delimiter) :]
                continue
            start_text = remaining_text[:first_delim]
            between_text = remaining_text[first_delim + len(delimiter) : second_delim]
            if second_delim != -1 and between_text.strip() == "":
                raise ValueError("Invalid markdown syntax")
            remaining_text = remaining_text[second_delim + len(delimiter) :]
            if start_text != "":
                new_nodes.append(TextNode(start_text, TextType.TEXT))
            new_nodes.append(TextNode(between_text, text_type))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        match = re.search(r"!\[(.*?)\]\((.*?)\)", text)
        while match:
            alt_text = match.group(1)
            image_link = match.group(2)
            start_text = text[: match.start()]
            end_text = text[match.end() :]
            if start_text != "":
                new_nodes.append(TextNode(start_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.TEXT))
            new_nodes.append(TextNode(image_link, TextType.IMAGE))
            text = end_text
            match = re.search(r"!\[(.*?)\]\((.*?)\)", text)
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        match = re.search(r"\[(.*?)\]\((.*?)\)", text)
        while match:
            link_text = match.group(1)
            link = match.group(2)
            start_text = text[: match.start()]
            end_text = text[match.end() :]
            if start_text != "":
                new_nodes.append(TextNode(start_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.TEXT))
            new_nodes.append(TextNode(" ", TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link))
            text = end_text
            match = re.search(r"\[(.*?)\]\((.*?)\)", text)
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def process_bold(nodes):
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            result.extend(split_nodes_delimiter([node], "**", TextType.BOLD))
        else:
            result.append(node)
    return result


def process_italic(nodes):
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            result.extend(split_nodes_delimiter([node], "*", TextType.ITALIC))
        else:
            result.append(node)
    return result


def process_code(nodes):
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            result.extend(split_nodes_delimiter([node], "`", TextType.CODE))
        else:
            result.append(node)
    return result


def process_link(nodes):
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            result.extend(split_nodes_link([node]))
        else:
            result.append(node)
    return result


def process_image(nodes):
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            result.extend(split_nodes_image([node]))
        else:
            result.append(node)
    return result


def text_to_textnodes(text):
    if text == "":
        return [TextNode("", TextType.TEXT)]
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = process_bold(nodes)
    nodes = process_italic(nodes)
    nodes = process_code(nodes)
    nodes = process_link(nodes)
    nodes = process_image(nodes)
    return nodes
