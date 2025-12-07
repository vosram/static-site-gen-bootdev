import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHTML(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic_to_html(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_text_link_to_html(self):
        node = TextNode("cool link node here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "cool link node here")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image_node_to_html(self):
        node = TextNode("cool image", TextType.IMAGE, "https://example.com/img_001.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/img_001.jpg")
        self.assertEqual(html_node.props["alt"], "cool image")


if __name__ == "__main__":
    unittest.main()
