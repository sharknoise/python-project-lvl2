"""Functions to build an AST."""

from typing import Any, Dict

ADDED = '+'
REMOVED = '-'
UNCHANGED = ' '
CHANGED = 'changed'
PARENT = 'parent'

TYPE = 'type'
VALUE = 'value'
OLD_VALUE = 'old_value'
NEW_VALUE = 'new_value'


def build_ast(
    old: Dict[str, Any], new: Dict[str, Any],
) -> Dict[str, Any]:  # noqa: WPS221 # WPS bug, line complexity in hints
    """Build an Abstract Syntax Tree for the difference between 2 dicts."""
    ast = {}

    old_keys = old.keys()
    new_keys = new.keys()
    removed_keys = old_keys - new_keys
    added_keys = new_keys - old_keys
    kept_keys = old_keys & new_keys

    for removed_key in removed_keys:
        ast[removed_key] = {
            TYPE: REMOVED,
            VALUE: old[removed_key],
        }

    for added_key in added_keys:
        ast[added_key] = {
            TYPE: ADDED,
            VALUE: new[added_key],
        }

    for kept_key in kept_keys:
        old_value = old[kept_key]
        new_value = new[kept_key]
        if old_value == new_value:
            ast[kept_key] = {
                TYPE: UNCHANGED,
                VALUE: old_value,
            }
        elif isinstance(old_value, dict) and isinstance(new_value, dict):
            ast[kept_key] = {
                TYPE: PARENT,
                VALUE: build_ast(
                    old_value, new_value,
                ),
            }
        elif old_value != new_value:
            ast[kept_key] = {
                TYPE: CHANGED,
                OLD_VALUE: old_value,
                NEW_VALUE: new_value,
            }
    return ast
