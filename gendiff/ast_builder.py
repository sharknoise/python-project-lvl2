"""Functions to build an AST."""

from typing import Any, Dict

ADDED = '+'
REMOVED = '-'
UNCHANGED = ' '
CHANGED = 'changed'
PARENT = 'parent'


def build_ast(
    old: Dict[str, Any], new: Dict[str, Any],
) -> Dict[str, Any]:  # noqa: WPS221 # WPS bug, line complexity in hints
    """Build an Abstract Syntax Tree for the difference between 2 dicts."""
    all_keys = list(old.keys() | new.keys())
    return {key: create_node(key, old, new) for key in all_keys}


def create_node(  # noqa: WPS231 # cognitive complexity isn't very high
    key: str, old: Dict[str, Any], new: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate an AST node."""
    new_value = new.get(key)
    old_value = old.get(key)
    if old_value is None:  # noqa: WPS223 # we use 4th elif to be explicit
        node = {
            'type': ADDED,
            'value': get_formatted(new_value),
        }
    elif new_value is None:
        node = {
            'type': REMOVED,
            'value': get_formatted(old_value),
        }
    elif isinstance(old_value, dict) and isinstance(new_value, dict):
        node = {
            'type': PARENT,
            'value': build_ast(old_value, new_value),
        }
    elif old_value == new_value:
        node = {
            'type': UNCHANGED,
            'value': get_formatted(old_value),
        }
    elif old_value != new_value:
        node = {
            'type': CHANGED,
            'old_value': get_formatted(old_value),
            'new_value': get_formatted(new_value),
        }
    return node


def get_formatted(unknown_type_value: Any):
    """Convert to lowercase str if the type is bool."""
    if unknown_type_value is True:
        return 'true'
    if unknown_type_value is False:
        return 'false'
    return unknown_type_value
