import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_html_with_props(self):
        node = LeafNode(
            "a",
            "My Awesome Website",
            {"href": "https://example.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank">My Awesome Website</a>',
        )

    def test_leaf_with_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), "Some text")

    def test_leaf_no_value_raise(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "pretty-bold"})
        child_node = ParentNode("span", [grandchild_node], {"class": "pretty-text"})
        parent_node = ParentNode(
            "div", [child_node], {"class": "container", "id": "root"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="root"><span class="pretty-text"><b class="pretty-bold">grandchild</b></span></div>',
        )

    def test_to_html_with_plaintext_grandchild(self):
        grandchild_node = LeafNode(None, "plain text grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>plain text grandchild</span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
