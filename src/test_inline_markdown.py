import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)


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
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
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
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
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
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_two_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/zjjcJKR.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another image", "https://i.imgur.com/zjjcJKR.png"),
            ],
            matches,
        )

    def test_extract_markdown_image_around_links(self):
        # This test has markdown images and markdown links
        # to see if it only picks up images and ignores the link
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). This is link text with a [python docs link](https://docs.python.org/3/index.html) and [go lang](https://go.dev)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [cool link](https://docs.python.org/3/index.html)"
        )
        self.assertListEqual(
            [("cool link", "https://docs.python.org/3/index.html")], matches
        )

    def test_extract_two_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [cool link](https://docs.python.org/3/index.html) and [another link](https://go.dev)"
        )
        self.assertListEqual(
            [
                ("cool link", "https://docs.python.org/3/index.html"),
                ("another link", "https://go.dev"),
            ],
            matches,
        )

    def test_extract_links_around_images(self):
        # This test has markdown images and markdown links
        # to see if it only picks up links and ignores the images
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). This is link text with a [python docs link](https://docs.python.org/3/index.html) and [go lang](https://go.dev)"
        )
        self.assertListEqual(
            [
                ("python docs link", "https://docs.python.org/3/index.html"),
                ("go lang", "https://go.dev"),
            ],
            matches,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [cool link](https://docs.python.org/3/index.html)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "cool link", TextType.LINK, "https://docs.python.org/3/index.html"
                ),
            ],
            new_nodes,
        )

    def test_split_link_text_on_end(self):
        node = TextNode(
            "This is text with a [cool link](https://docs.python.org/3/index.html), what do you think?",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "cool link", TextType.LINK, "https://docs.python.org/3/index.html"
                ),
                TextNode(", what do you think?", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_2_links(self):
        node = TextNode(
            "This is text with an [cool link](https://docs.python.org/3/index.html) and another [second link](https://go.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "cool link", TextType.LINK, "https://docs.python.org/3/index.html"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://go.dev"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_text_on_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(", and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), and some text",
            TextType.TEXT,
        )
        node_2 = TextNode("<p>awesome</p>", TextType.CODE)
        node_3 = TextNode(
            "This ![bird](https://example.com/img_bird_001.jpg) is cool", TextType.TEXT
        )
        new_nodes = split_nodes_image([node, node_2, node_3])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(", and some text", TextType.TEXT),
                TextNode("<p>awesome</p>", TextType.CODE),
                TextNode("This ", TextType.TEXT),
                TextNode(
                    "bird", TextType.IMAGE, "https://example.com/img_bird_001.jpg"
                ),
                TextNode(" is cool", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result_nodes,
        )

    def test_text_to_textnodes_2(self):
        text = "Another **example** of the _power_ of `markdown.md` to static html. Including ![cool images](https://images.example.com/img_001.jpg) and some [awesome links](https://example.com/about), cool huh?"
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Another ", TextType.TEXT),
                TextNode("example", TextType.BOLD),
                TextNode(" of the ", TextType.TEXT),
                TextNode("power", TextType.ITALIC),
                TextNode(" of ", TextType.TEXT),
                TextNode("markdown.md", TextType.CODE),
                TextNode(" to static html. Including ", TextType.TEXT),
                TextNode(
                    "cool images",
                    TextType.IMAGE,
                    "https://images.example.com/img_001.jpg",
                ),
                TextNode(" and some ", TextType.TEXT),
                TextNode("awesome links", TextType.LINK, "https://example.com/about"),
                TextNode(", cool huh?", TextType.TEXT),
            ],
            result_nodes,
        )

    def test_text_to_textnodes_invalid_markdown(self):
        text = "This markdown text has **an invalid markdown syntax"

        with self.assertRaises(ValueError):
            nodes = text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()
