from enum import Enum
import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str):
    # according to the docs, re.match searches the start or the line
    # so i don't think i need a ^ char in front of the regex pattern
    # to specify the pattern is at the start of the text
    # https://docs.python.org/3/library/re.html#re.match

    lines = block.split("\n")

    if re.match(r"#{1,6}\s", block):
        return BlockType.HEADING
    elif len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root_html_node = ParentNode("div", [])
    for block in blocks:
        # block here is just a string
        block_type = block_to_block_type(block)
        # block_type identifies the type of block it is
        # i.e. heading, paragraph, ordered_list

        match block_type:
            case BlockType.HEADING:
                html_node = heading_to_html_node(block)
                root_html_node.children.append(html_node)

            case BlockType.CODE:
                pre_node = code_to_html_node(block)
                root_html_node.children.append(pre_node)

            case BlockType.ORDERED_LIST:
                ol_node = olist_to_html_node(block)
                root_html_node.children.append(ol_node)

            case BlockType.UNORDERED_LIST:
                ul_node = ulist_to_html_node(block)
                root_html_node.children.append(ul_node)

            case BlockType.QUOTE:
                quote_node = blockquote_to_html_node(block)
                root_html_node.children.append(quote_node)

            case BlockType.PARAGRAPH:
                paragraph_html_node = paragraph_to_html_node(block)
                root_html_node.children.append(paragraph_html_node)

            case _:
                pass

    return root_html_node


def blockquote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("> ").strip())
    html_qoute_node = ParentNode("blockquote", [])
    content = " ".join(new_lines)
    text_nodes = text_to_textnodes(content)
    html_child_nodes = []
    for text_node in text_nodes:
        html_child_nodes.append(text_node_to_html_node(text_node))
    blockquote_node = ParentNode("blockquote", html_child_nodes)
    return blockquote_node


def heading_to_html_node(block):
    hashtags = re.match(r"#{1,6}\s", block)[0]
    num = 0

    for char in hashtags:
        if char == "#":
            num += 1

    heading_value = block.split("# ", 1)[1]
    html_node = LeafNode(f"h{num}", heading_value)
    return html_node


def ulist_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []

    for line in lines:
        new_line = line.lstrip("- ").strip()
        text_nodes = text_to_textnodes(new_line)
        li_node = ParentNode("li", [])
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            li_node.children.append(html_node)
        html_nodes.append(li_node)

    ul_html_node = ParentNode("ul", html_nodes)

    return ul_html_node


def olist_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    count = 1
    for line in lines:
        new_line = line.lstrip(f"{count}. ").strip()
        text_nodes = text_to_textnodes(new_line)
        li_node = ParentNode("li", [])
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            li_node.children.append(html_node)
        html_nodes.append(li_node)
        count += 1

    ol_html_node = ParentNode("ol", html_nodes)

    return ol_html_node


def code_to_html_node(block):
    text_value = block.split("```\n", 1)[1].split("```", 1)[0]
    text_node = TextNode(text_value, TextType.CODE)
    code_node = text_node_to_html_node(text_node)
    pre_node = ParentNode("pre", [code_node])
    return pre_node


def paragraph_to_html_node(block):
    leaf_nodes = []
    lines = block.split("\n")
    new_line = " ".join(lines)
    text_nodes = text_to_textnodes(new_line)
    for node in text_nodes:
        leaf_node = text_node_to_html_node(node)
        leaf_nodes.append(leaf_node)
    p_node = ParentNode("p", leaf_nodes)
    return p_node
