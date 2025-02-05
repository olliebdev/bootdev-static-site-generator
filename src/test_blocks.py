import unittest
from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    text_to_children,
)
from htmlnode import HTMLNode
from textnode import text_node_to_html_node, TextNode


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "Hello\n\nWorld"
        expected = ["Hello", "World"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace_blocks(self):
        markdown = "  Hello  \n\n  World  "
        expected = ["Hello", "World"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blank_lines(self):
        markdown = "Block1\n\n\n\n\nBlock2"
        expected = ["Block1", "Block2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_document(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block(self):
        markdown = "Just one block"
        expected = ["Just one block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace_only_blocks(self):
        markdown = "Block1\n\n    \n\nBlock2"
        expected = ["Block1", "Block2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_blanks(self):
        markdown = "\n\nBlock1\n\nBlock2\n\n"
        expected = ["Block1", "Block2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    # block to block type
    def test_basic_paragraph(self):
        markdown = "This is a paragraph with some *italic* text."
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "p")

    def test_headings(self):
        markdown = "# H1 Heading\n## H2 Heading\n### H3 Heading"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "h2")
        self.assertEqual(node.children[2].tag, "h3")
        self.assertEqual(node.children[0].children[0].text, "H1 Heading")

    def test_blockquote(self):
        markdown = ">This is a quote\n>With multiple lines"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "blockquote")

    def test_code_blocks(self):
        # Basic code block
        markdown = "```\ndef hello():\n    print('Hello')\n```"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "pre")
        self.assertEqual(html.children[0].children[0].tag, "code")

        # Code block with language
        markdown = "```python\nprint('hello')\nprint('world')\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(node.children[0].children[0].tag, "code")
        code_content = node.children[0].children[0].children[0].text
        self.assertEqual(code_content, "python\nprint('hello')\nprint('world')")

    def test_unordered_lists(self):
        # Basic unordered list
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "ul")
        self.assertEqual(len(html.children[0].children), 3)
        self.assertEqual(html.children[0].children[0].tag, "li")

        # Unordered list with formatting
        markdown = "* **Bold** item\n* *Italic* item\n* `code` item"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        ul_node = node.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 3)
        self.assertEqual(ul_node.children[0].tag, "li")

    def test_ordered_lists(self):
        markdown = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        ol_node = node.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)

    def test_mixed_content(self):
        markdown = "# Heading\n\nParagraph\n\n* List item"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "h1")

    def test_multiple_paragraphs(self):
        markdown = "First paragraph\n\nSecond paragraph\n\nThird paragraph"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "p")
        self.assertEqual(node.children[0].children[0].text, "First paragraph")
        self.assertEqual(node.children[1].children[0].text, "Second paragraph")

    def test_empty_blocks(self):

        # Empty ordered list items
        markdown = "1. \n2. Item\n3. "
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "ol")
        self.assertEqual(len(node.children[0].children), 3)

        # Empty code block
        markdown = "```\n\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(len(node.children[0].children), 1)
        self.assertEqual(node.children[0].children[0].tag, "code")
        self.assertEqual(node.children[0].children[0].children[0].text, "\n")

        # Empty list items

    def test_empty_list_items(self):
        markdown = "* \n* Item\n* "
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(len(node.children[0].children), 3)
        self.assertEqual(node.children[0].children[0].tag, "li")
        self.assertEqual(node.children[0].children[1].children[0].text, "Item")
        self.assertEqual(len(node.children[0].children[0].children), 0)
