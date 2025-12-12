import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
