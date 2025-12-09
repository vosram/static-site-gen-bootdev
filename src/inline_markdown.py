from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        text_segments = node.text.split(delimiter)

        if len(text_segments) % 2 == 0:
            raise ValueError("a delimiter was not paired up in the text")

        for i in range(len(text_segments)):
            if text_segments[i] == "":
                continue
            if i % 2 == 0:
                new_node = TextNode(text_segments[i], node.text_type, node.url)
                new_list.append(new_node)
            else:
                new_node = TextNode(text_segments[i], text_type, node.url)
                new_list.append(new_node)
    return new_list


def extract_markdown_images(text):
    # bootdev provided regex r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # my regex r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    # bootdev provided regex r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # my regex r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
