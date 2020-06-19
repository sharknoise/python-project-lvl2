"""Functions that render a diff AST as plain text."""

from typing import Any, Dict

from gendiff.ast import ADDED, CHANGED, PARENT, REMOVED


def plain_format(ast: Dict[str, Any], property_path='') -> str:
    """
    Render a diff Abstract Syntax Tree as plain text.

    Args:
        property_path: which nodes lead to this part of the tree;
            we change the default when we call the function
            recursively to render a part of the tree
        ast: a dict built by gendiff.ast.build_tree

    Returns:
        a multiline string describing the difference
    """
    diff = []

    for node_key, node_value in sorted(ast.items()):

        full_property_name = property_path + node_key
        item_type = node_value.get('type')
        item_value = node_value.get('value')

        if item_type == PARENT:
            diff.append(plain_format(
                item_value,
                full_property_name + '.',  # noqa: WPS336 # + for readability
            ))
        elif item_type == CHANGED:
            old_value = node_value.get('old_value')
            new_value = node_value.get('new_value')
            diff.append(
                "Property '{0}' was changed from '{1}' to '{2}'".format(
                    full_property_name, old_value, new_value,
                ),
            )
        elif item_type == REMOVED:
            diff.append("Property '{0}' was removed".format(
                full_property_name,
            ))
        elif item_type == ADDED:
            diff.append("Property '{0}' was added with value '{1}'".format(
                full_property_name, get_formatted(item_value),
            ))
        # we don't render item_type == UNCHANGED in this renderer
    return '\n'.join(diff)


def get_formatted(unknown_type_value):
    """Replace with str description when the argument is a dict."""
    if isinstance(unknown_type_value, dict):
        return 'complex value'
    return unknown_type_value
