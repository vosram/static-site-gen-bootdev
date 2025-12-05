import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_class_props_eq(self):
        node = HTMLNode("p", "this is some text", None, {"class": "pretty-paragraph"})
        self.assertEqual(node.props_to_html(), ' class="pretty-paragraph"')

    def test_a_link_props_eq(self):
        node = HTMLNode(
            "a",
            "this is a link",
            None,
            {"href": "www.example.com/about", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="www.example.com/about" target="_blank"'
        )

    def test_no_props_eq(self):
        node = HTMLNode("h1", "heading 1")
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props_eq(self):
        node = HTMLNode("h1", "heading 1", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_all_values(self):
        node = HTMLNode("h1", "A Wonderful Heading")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "A Wonderful Heading")
        self.assertEqual(node.children, None)
        self.assertEqual(node.children, None)

    def test_repr(self):
        node = HTMLNode("p", "a paragraph")
        self.assertEqual(node.__repr__(), "HTMLNode(p, a paragraph, None, None)")


if __name__ == "__main__":
    unittest.main()
