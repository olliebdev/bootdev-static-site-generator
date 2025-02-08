import unittest
from extract import extract_markdown_images, extract_markdown_links, extract_title


class TestExtract(unittest.TestCase):
    def test_extract_images(self):
        text = "Here's an ![example image](http://example.com/img.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result[0], ("example image", "http://example.com/img.jpg"))

    def test_extract_links(self):
        text = "Here's a [example link](http://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result[0], ("example link", "http://example.com"))

    def test_multiple_images(self):
        text = "![first](http://first.com) and ![second](http://second.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result[0], ("first", "http://first.com"))
        self.assertEqual(result[1], ("second", "http://second.com"))

    def test_no_matches(self):
        text = "Just plain text with no markdown"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_mixed_content(self):
        text = "Here's a ![image](http://img.com) and a [link](http://link.com)"
        result_images = extract_markdown_images(text)
        result_links = extract_markdown_links(text)
        self.assertEqual(result_images[0], ("image", "http://img.com"))
        self.assertEqual(result_links[0], ("link", "http://link.com"))

    # Title
    def test_extract_title(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
        markdown = "## Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")


if __name__ == "__main__":
    unittest.main()
