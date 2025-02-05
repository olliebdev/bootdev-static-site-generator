import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "test text", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "test text", None, {"href": "https://www.google.com"})
        self.assertEqual(node.tag, node2.tag)

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_single_prop(self):
        node = HTMLNode(props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_multiple_props(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode("p", "test text")
        self.assertEqual(
            "HTMLNode(tag='p', text='test text', children='None', props=None)",
            repr(node),
        )


class TestLeafNode(unittest.TestCase):
    def test_basic_leaf(self):
        node = LeafNode(tag="p", text="this is a paragraph")
        self.assertEqual(node.to_html(), "<p>this is a paragraph</p>")

    def test_leaf_with_props(self):
        node = LeafNode(
            tag="a",
            text="Click me",
            props={"href": "https://example.com", "class": "link"},
        )
        self.assertEqual(
            node.to_html(), '<a href="https://example.com" class="link">Click me</a>'
        )

    def test_raw_text(self):
        node = LeafNode(tag=None, text="test text", props=None)
        self.assertEqual(node.to_html(), "test text")

    def test_none_text(self):
        node = LeafNode(tag=None, text=None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_parent_one_leaf(self):
        parent = ParentNode("div", [LeafNode("p", "hello")])
        self.assertEqual(parent.to_html(), "<div><p>hello</p></div>")

    def test_missing_tag(self):
        parent = ParentNode(None, [LeafNode("p", "hello")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_missing_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_multiple_children(self):
        parent = ParentNode(
            "div",
            [LeafNode("b", "bold"), LeafNode(None, "normal"), LeafNode("i", "italic")],
        )
        self.assertEqual(parent.to_html(), "<div><b>bold</b>normal<i>italic</i></div>")

    def test_nested_parents(self):
        parent = ParentNode("div", [ParentNode("p", [LeafNode("b", "bold text")])])
        self.assertEqual(parent.to_html(), "<div><p><b>bold text</b></p></div>")


if __name__ == "__main__":
    unittest.main()
