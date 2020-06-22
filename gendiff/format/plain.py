"""Functions that render a diff AST as plain text."""

from typing import Any, Dict

from gendiff import ast


def plain_format(diff_tree: Dict[str, Any]) -> str:
    """
    Render a diff Abstract Syntax Tree as plain text.

    Args:
        diff_tree: a dict built by gendiff.ast.build_tree

    Returns:
        a multiline string describing the difference
    """
    lines = []

    def walk(tree_part, property_path):  # noqa: WPS430 # used to add 2nd arg
        # property_path: which nodes lead to this part of the tree
        for node_key, node_value in sorted(tree_part.items()):
            full_property_name = property_path + node_key
            item_type = node_value[ast.TYPE]
            if item_type == ast.PARENT:
                item_value = node_value[ast.VALUE]
                walk(
                    item_value,
                    full_property_name + '.',  # noqa: WPS336 # + more readable
                )
            elif item_type == ast.CHANGED:
                old_value = node_value[ast.OLD_VALUE]
                new_value = node_value[ast.NEW_VALUE]
                lines.append(
                    "Property '{0}' was changed from '{1}' to '{2}'".format(
                        full_property_name, old_value, new_value,
                    ),
                )
            elif item_type == ast.REMOVED:
                lines.append("Property '{0}' was removed".format(
                    full_property_name,
                ))
            elif item_type == ast.ADDED:
                if isinstance(node_value[ast.VALUE], dict):
                    item_value = 'complex value'
                else:
                    item_value = node_value[ast.VALUE]
                lines.append(
                    "Property '{0}' was added with value '{1}'".format(
                        full_property_name, item_value,
                    ),
                )
            # we don't render item_type == ast.UNCHANGED in this formatter

    walk(diff_tree, property_path='')

    return '\n'.join(lines)
