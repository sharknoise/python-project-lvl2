"""Functions that render a lines AST as a jsonlike string."""

from typing import Any, Dict

from gendiff import ast

INDENT = '  '
marks = {ast.ADDED: '+', ast.REMOVED: '-', ast.UNCHANGED: ' '}
LINE_TEMPLATE = '{indent}{mark} {key}: {value}'


def default_format(diff_tree: Dict[str, Any]) -> str:
    """
    Render a lines Abstract Syntax Tree as a jsonlike string.

    Args:
        diff_tree: a dict built by genlines.ast.build_tree
            or one of the nested dicts that represents a
            part of the tree

    Returns:
        a multiline string with jsonlike syntax
    """
    lines = []

    def walk(tree, depth):  # noqa: WPS430 # we use closure to add 2nd arg
        # depth: whole tree starts from depth 1, nested tree parts start deeper
        indent = INDENT * depth
        for node_key, node_value in sorted(tree.items()):
            item_type = node_value[ast.TYPE]
            # we use get as CHANGED nodes have other keys instead of VALUE
            item_value = node_value.get(ast.VALUE)
            if item_type == ast.PARENT:
                lines.append('{indent}{mark} {key}: {{'.format(
                    indent=indent,
                    mark=marks[ast.UNCHANGED],
                    key=node_key,
                ))
                walk(item_value, depth + 2)
                lines.append('{indent}}}'.format(indent=indent + INDENT))
            elif item_type == ast.CHANGED:
                old_value = node_value[ast.OLD_VALUE]
                new_value = node_value[ast.NEW_VALUE]
                lines.append(LINE_TEMPLATE.format(
                    indent=indent,
                    mark=marks[ast.REMOVED],
                    key=node_key,
                    value=old_value,
                ))
                lines.append(LINE_TEMPLATE.format(
                    indent=indent,
                    mark=marks[ast.ADDED],
                    key=node_key,
                    value=new_value,
                ))
            elif item_type in {ast.ADDED, ast.REMOVED, ast.UNCHANGED}:
                if isinstance(item_value, dict):
                    item_value = format_block(item_value, indent)
                lines.append(LINE_TEMPLATE.format(
                    indent=indent,
                    mark=marks[item_type],
                    key=node_key,
                    value=item_value,
                ))

    walk(diff_tree, depth=1)

    lines = ['{'] + lines + ['}']
    return '\n'.join(lines)


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
        block_lines.append(LINE_TEMPLATE.format(
            indent=property_indent,
            mark=marks[ast.UNCHANGED],
            key=property_name,
            value=property_value,
        ))
    block_lines.append('{indent}}}'.format(indent=clos_bracket_indent))
    return '\n'.join(block_lines)
