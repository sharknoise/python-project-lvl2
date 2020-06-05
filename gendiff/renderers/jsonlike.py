"""Functions that renders a diff AST as a jsonlike string."""

from typing import Any, Dict

from gendiff.ast_builder import ADDED, CHANGED, CHILD, REMOVED, UNCHANGED

INDENT = '  '


def jsonlike_render(ast: Dict[str, Any], depth=1) -> str:
    """
    Render a diff Abstract Syntax Tree as a jsonlike string.

    Args:
        ast: a dict built by gendiff.ast_builder.build_ast
        depth: the level of jsonlike nesting

    Returns:
        a multiline string with jsonlike syntax
    """
    diff = []
    indent = INDENT * depth
    for node_key, node_value in ast.items():
        item_type = node_value.get('type')
        item_value = node_value.get('value')
        if item_type == CHANGED:
            item_old = node_value.get('old_value')
            item_new = node_value.get('new_value')
            diff.append(format_node(indent, REMOVED, node_key, item_old))
            diff.append(format_node(indent, ADDED, node_key, item_new))
        elif item_type == CHILD:
            diff.append('{indent}{sign} {key}: {{'.format(
                indent=indent,
                sign=UNCHANGED,
                key=node_key,
            ))
            diff.append(jsonlike_render(item_value, depth + 2))
            diff.append('{indent}}}'.format(indent=indent + INDENT))
        elif item_type in {ADDED, REMOVED, UNCHANGED}:
            diff.append(format_node(
                indent,
                item_type,
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


def format_node(indent: int, sign: str, node_key, node_value) -> str:
    """Convert a leaf node into a single line string."""
    return '{indent}{sign} {node_key}: {node_value}'.format(
        indent=indent,
        sign=sign,
        node_key=str(node_key),
        node_value=str(node_value),
    )


def format_block(properties: dict, block_indent: str) -> str:
    """
    Convert all properties of a node into a multiline string.

    Args:
        properties: a group of properties that don't have their own node_type
                   as they were ADDED, REMOVED, CHANGED as a part of one node
        block_indent: the indent of this node

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
            UNCHANGED,
            property_name,
            property_value,
        ))
        block_lines.append('{indent}}}'.format(indent=clos_bracket_indent))
    return '\n'.join(block_lines)
