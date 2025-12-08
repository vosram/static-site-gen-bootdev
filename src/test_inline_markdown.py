import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_code_block_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type.value, "code")
        self.assertEqual(new_nodes[2].text, " word")

    def test_bold_block_split(self):
        node = TextNode("This is text with a **bold text** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_2_bold_in_1_node_split(self):
        node = TextNode("This is **text** with a **bold text** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " with a ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "bold text")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " word")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_odd_num_of_delimiter(self):
        node = TextNode("This is **text** with a **bold text word", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_3_nodes_demiliter(self):
        node_1 = TextNode(
            "This is the first text with an _italic text_ word", TextType.TEXT
        )
        node_2 = TextNode(
            "This is the second text with an _italic text_ word", TextType.TEXT
        )
        node_3 = TextNode(
            "This is the third text with an _italic text_ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter(
            [node_1, node_2, node_3], "_", TextType.ITALIC
        )
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is the first text with an ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "This is the second text with an ")
        self.assertEqual(new_nodes[4].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, "italic text")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, " word")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[6].text, "This is the third text with an ")
        self.assertEqual(new_nodes[7].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[7].text, "italic text")
        self.assertEqual(new_nodes[8].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[8].text, " word")

    def test_non_text_nodes_delimiter(self):
        node_1 = TextNode(
            "This is the first text with an _italic text_ word", TextType.TEXT
        )
        node_2 = TextNode("link to cool website", TextType.LINK, "https://example.com")
        node_3 = TextNode(
            "This is the second text with an _italic text_ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter(
            [node_1, node_2, node_3], "_", TextType.ITALIC
        )
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is the first text with an ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, "link to cool website")
        self.assertEqual(new_nodes[3].url, "https://example.com")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "This is the second text with an ")
        self.assertEqual(new_nodes[5].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[5].text, "italic text")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[6].text, " word")

    # Boot.dev test
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
