"""Functions that render a diff AST as a jsonlike string."""

from typing import Any, Dict

from gendiff.ast import ADDED, CHANGED, PARENT, REMOVED, UNCHANGED

INDENT = '  '
marks = {ADDED: '+', REMOVED: '-', UNCHANGED: ' '}


def default_format(ast: Dict[str, Any], depth=1) -> str:
    """
    Render a diff Abstract Syntax Tree as a jsonlike string.

    Args:
        ast: a dict built by gendiff.ast.build_tree
            or one of the nested dicts that represents a
            part of the tree
        depth: the level of jsonlike nesting, we change it
            when we call the function recursively to render
            a part of the tree

    Returns:
        a multiline string with jsonlike syntax
    """
    diff = []
    indent = INDENT * depth
    for node_key, node_value in sorted(ast.items()):
        item_type = node_value.get('type')
        item_value = node_value.get('value')
        if item_type == CHANGED:
            old_value = node_value.get('old_value')
            new_value = node_value.get('new_value')
            diff.append(
                format_node(indent, marks[REMOVED], node_key, old_value),
            )
            diff.append(
                format_node(indent, marks[ADDED], node_key, new_value),
            )
        elif item_type == PARENT:
            diff.append('{indent}{sign} {key}: {{'.format(
                indent=indent,
                sign=marks[UNCHANGED],
                key=node_key,
            ))
            diff.append(default_format(item_value, depth + 2))
            diff.append('{indent}}}'.format(indent=indent + INDENT))
        elif item_type in {ADDED, REMOVED, UNCHANGED}:
            diff.append(format_node(
                indent,
                marks[item_type],
                node_key,
                get_formatted(item_value, indent),
            ))
    if depth == 1:
        diff = ['{'] + diff + ['}']
    return '\n'.join(diff)


def get_formatted(element, indent):
    """Return value as 1 item or a block of lines in curly brackets."""
    if isinstance(element, dict):
        return format_block(element, indent)
    return element


def format_node(indent: str, sign: str, node_key, node_value) -> str:
    """Convert a leaf node into a string."""
    return '{indent}{sign} {node_key}: {node_value}'.format(
        indent=indent,
        sign=sign,
        node_key=node_key,
        node_value=node_value,
    )


def format_block(properties: dict, block_indent: str) -> str:
    """
    Convert a complex value of a node into a multiline string.

    Args:
        properties: a group of properties that aren't represented
            as separate nodes in the AST, because they were added,
            removed or changed as a part of one node
        block_indent: the indent of this node's key name

    Returns:
        a multiline string with the block of properties inside curly brackets
    """
    block_lines = []
    block_lines.append('{')
    property_indent = block_indent + INDENT*2
    clos_bracket_indent = block_indent + INDENT
    for property_name, property_value in properties.items():
        block_lines.append(format_node(
            property_indent,
            marks[UNCHANGED],
            property_name,
            property_value,
        ))
        block_lines.append('{indent}}}'.format(indent=clos_bracket_indent))
    return '\n'.join(block_lines)
