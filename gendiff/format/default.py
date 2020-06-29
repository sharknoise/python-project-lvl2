"""Functions that render a lines AST as a jsonlike string."""

from typing import Any, Dict

from gendiff import ast

INDENT = '  '
get_mark = {ast.ADDED: '+', ast.REMOVED: '-', ast.UNCHANGED: ' '}.get
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
                    mark=get_mark(ast.UNCHANGED),
                    key=node_key,
                ))
                walk(item_value, depth + 2)
                lines.append('{indent}}}'.format(indent=indent + INDENT))
            elif item_type == ast.CHANGED:
                old_value = node_value[ast.OLD_VALUE]
                new_value = node_value[ast.NEW_VALUE]
                lines.append(LINE_TEMPLATE.format(
                    indent=indent,
                    mark=get_mark(ast.REMOVED),
                    key=node_key,
                    value=old_value,
                ))
                lines.append(LINE_TEMPLATE.format(
                    indent=indent,
                    mark=get_mark(ast.ADDED),
                    key=node_key,
                    value=new_value,
                ))
            elif item_type in {ast.ADDED, ast.REMOVED, ast.UNCHANGED}:
                if isinstance(item_value, dict):
                    # then it's a group of properties that aren't represented
                    # as separate nodes in the AST, because they were added,
                    # removed or changed as a part of one node,
                    # but the project task is to format them as multiple lines
                    lines.append(  # group name and the opening bracket
                        '{indent}{mark} {key}: {{'.format(
                            indent=indent,
                            mark=get_mark(item_type),
                            key=node_key,
                        ))
                    for property_name, property_value in item_value.items():
                        lines.append(LINE_TEMPLATE.format(
                            indent=indent + INDENT*2,
                            mark=get_mark(ast.UNCHANGED),
                            key=property_name,
                            value=property_value,
                        ))
                    lines.append(  # closing bracket of the group
                        '{indent}}}'.format(indent=indent + INDENT),
                    )
                else:
                    lines.append(LINE_TEMPLATE.format(
                        indent=indent,
                        mark=get_mark(item_type),
                        key=node_key,
                        value=item_value,
                    ))

    walk(diff_tree, depth=1)

    lines = ['{'] + lines + ['}']
    return '\n'.join(lines)
