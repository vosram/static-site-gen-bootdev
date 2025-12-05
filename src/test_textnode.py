import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is one text", TextType.ITALIC)
        node2 = TextNode("This is another text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is one text", TextType.BOLD)
        node2 = TextNode("This is one text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode(
            "This is one text", TextType.LINK, "https://example.com/img_001"
        )
        node2 = TextNode(
            "This is one text", TextType.LINK, "https://example.com/img_002"
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
