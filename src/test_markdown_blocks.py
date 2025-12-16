import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    maxDiff = None

    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
# Cool heading 1

Some lovely paragraph **content** with great information

- ordered topic
- with another topic
- and yet another topic

## heading for the unordered?

1. yeah you guessed it
2. this would be an ordered list
3. Ain't that something

```
def lets_start_coding(here):
    pass
```

## last words here

> And thus concludes with my final quote
"""

        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                block_to_block_type(blocks[0]),
                block_to_block_type(blocks[1]),
                block_to_block_type(blocks[2]),
                block_to_block_type(blocks[3]),
                block_to_block_type(blocks[4]),
                block_to_block_type(blocks[5]),
                block_to_block_type(blocks[6]),
                block_to_block_type(blocks[7]),
            ],
            [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.HEADING,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.HEADING,
                BlockType.QUOTE,
            ],
        )

    def test_block_to_block_type_wrong_syntax(self):
        md = """
# Cool heading 1

Some lovely paragraph **content** with great information

- ordered topic
with another topic
- and yet another topic

## heading for the unordered?

1. yeah you guessed it
7. this would be an ordered list
3. Ain't that something

```
def lets_start_coding(here):
    pass
```

## last words here

> And thus concludes with my final quote
"""

        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                block_to_block_type(blocks[0]),
                block_to_block_type(blocks[1]),
                block_to_block_type(blocks[2]),
                block_to_block_type(blocks[3]),
                block_to_block_type(blocks[4]),
                block_to_block_type(blocks[5]),
                block_to_block_type(blocks[6]),
                block_to_block_type(blocks[7]),
            ],
            [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.HEADING,
                BlockType.QUOTE,
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings_with_lists(self):
        md = """
# Cool Blog Article

We will dive deep into this subject.

- point 1
- point 2

## Other Talking Points?

1. Yeah, this one
2. and this one
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Cool Blog Article</h1><p>We will dive deep into this subject.</p><ul><li>point 1</li><li>point 2</li></ul><h2>Other Talking Points?</h2><ol><li>Yeah, this one</li><li>and this one</li></ol></div>",
        )

    def test_full_md_to_html_content_1(self):
        md = """
# Cool heading 1

Some lovely paragraph **content** with great information

- unordered topic
- with another topic
- and yet another topic

## heading for the unordered?

1. yeah you guessed it
2. this would be an ordered list
3. Ain't that something

```
def lets_start_coding(here):
    pass
```

## last words here

> And thus concludes with my final quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Cool heading 1</h1><p>Some lovely paragraph <b>content</b> with great information</p><ul><li>unordered topic</li><li>with another topic</li><li>and yet another topic</li></ul><h2>heading for the unordered?</h2><ol><li>yeah you guessed it</li><li>this would be an ordered list</li><li>Ain't that something</li></ol><pre><code>def lets_start_coding(here):\n    pass\n</code></pre><h2>last words here</h2><blockquote>And thus concludes with my final quote</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
