import unittest
from textnode import TextNode, TextType

from split import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplit(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_list)

    def test_multi_code_block(self):
        node = TextNode(
            "This is text with a `code block` word and `another code block`",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, test_list)

    def test_non_text_node(self):
        node = TextNode("This is already code", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([node], new_nodes)

    def test_only_delimited_content(self):
        node = TextNode("`only code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([TextNode("only code", TextType.CODE)], new_nodes)

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    # img split
    def test_image_no_md(self):
        node = TextNode("No markdown here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "No markdown here")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_image_single_md(self):
        node = TextNode("Text before ![alt](http://link.com) text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Text before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link.com")
        self.assertEqual(new_nodes[2].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, " text after")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)

    def test_image_multi_md(self):
        node = TextNode(
            "Before ![alt1](http://link1.com) middle ![alt2](http://link2.com) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "Before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt1")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link1.com")
        self.assertEqual(new_nodes[2].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, " middle ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "alt2")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "http://link2.com")
        self.assertEqual(new_nodes[5].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[6].text, " after")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)

    def test_image_markdown_at_start(self):
        node = TextNode(
            "![alt](http://link.com) rest of text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "alt")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "http://link.com")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[2].text, " rest of text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_image_markdown_at_end(self):
        node = TextNode(
            "Text before ![alt](http://link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link.com")
        self.assertEqual(new_nodes[2].text_type, TextType.IMAGE)

    def test_consecutive_image_markdowns(self):
        node = TextNode(
            "Text ![alt](http://link.com)![alt2](http://another.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link.com")
        self.assertEqual(new_nodes[2].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, "alt2")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "http://another.com")
        self.assertEqual(new_nodes[4].text_type, TextType.IMAGE)

    # split link
    def test_link_no_md(self):
        node = TextNode("No markdown here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "No markdown here")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_link_single_md(self):
        node = TextNode("Text before [text](http://link.com) text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Text before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link.com")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, " text after")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)

    def test_link_multi_md(self):
        node = TextNode(
            "Before [text1](http://link1.com) middle [text2](http://link2.com) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "Before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text1")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link1.com")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, " middle ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "text2")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "http://link2.com")
        self.assertEqual(new_nodes[5].text_type, TextType.LINK)
        self.assertEqual(new_nodes[6].text, " after")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)

    def test_link_markdown_at_start(self):
        node = TextNode(
            "[text](http://link.com) rest of text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "http://link.com")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text, " rest of text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_link_markdown_at_end(self):
        node = TextNode(
            "Text before [text](http://link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link.com")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)

    def test_consecutive_link_markdowns(self):
        node = TextNode(
            "Text [text](http://link.com)[text2](http://another.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "http://link.com")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, "text2")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "http://another.com")
        self.assertEqual(new_nodes[4].text_type, TextType.LINK)

    # Text to text nodes

    def test_text_to_textnodes(self):
        self.assertEqual(
            text_to_textnodes("Simple text"), [TextNode("Simple text", TextType.TEXT)]
        )

        self.assertEqual(
            text_to_textnodes("This is **bold** text"),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

        nodes = text_to_textnodes("This is **bold** and *italic* with `code`")
        self.assertEqual(len(nodes), 6)

        nodes = text_to_textnodes(
            "This is a [link](https://boot.dev) and ![image](test.jpg)"
        )
        self.assertEqual(len(nodes), 6)

        self.assertEqual(text_to_textnodes(""), [TextNode("", TextType.TEXT)])

        self.assertEqual(
            text_to_textnodes("Simple text"), [TextNode("Simple text", TextType.TEXT)]
        )

    def test_split_nodes_delimiter(self):
        # Test simple italic
        node = TextNode("hello *world* test", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "hello ")
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " test")

        # Test just italic word
        node = TextNode("*world*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "world")
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)

        # Test multiple italic sections
        node = TextNode("*one* normal *two*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)


if __name__ == "__main__":
    unittest.main()
