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


type TextNodeList = list[TextNode]


def split_nodes_link(nodes: TextNodeList):
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.TEXT:
            # if node is not a text node, just add it to return list
            new_nodes.append(node)
            continue

        link_data = extract_markdown_links(node.text)
        if len(link_data) == 0:
            # if there are no links, just append the current node as is
            new_nodes.append(node)
            continue

        links_nodes = node_split_helper(node, link_data, TextType.LINK)
        new_nodes.extend(links_nodes)
    return new_nodes


def split_nodes_image(nodes: TextNodeList):
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.TEXT:
            # if node is not a text node, just add it to return list
            new_nodes.append(node)
            continue

        link_data = extract_markdown_images(node.text)
        if len(link_data) == 0:
            # if there are no links, just append the current node as is
            new_nodes.append(node)
            continue

        links_nodes = node_split_helper(node, link_data, TextType.IMAGE)
        new_nodes.extend(links_nodes)
    return new_nodes


def node_split_helper(node, link_data, special_type):
    links_nodes = []
    node_text = node.text

    for alt_text, url in link_data:
        split_pattern = None

        if special_type == TextType.LINK:
            split_pattern = f"[{alt_text}]({url})"
        elif special_type == TextType.IMAGE:
            split_pattern = f"![{alt_text}]({url})"

        text_segments = node_text.split(split_pattern, 1)
        if len(text_segments) != 2:
            raise ValueError(
                f"invalid mardown, {special_type.value} section not closed"
            )

        if text_segments[0] != "":
            links_nodes.append(TextNode(text_segments[0], TextType.TEXT))

        links_nodes.append(TextNode(alt_text, special_type, url))

        node_text = text_segments[1]

    if node_text != "":
        links_nodes.append(TextNode(node_text, TextType.TEXT))
    return links_nodes
