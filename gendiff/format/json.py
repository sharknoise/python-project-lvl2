"""Functions that render as JSON."""

import json


def json_format(diff_tree):
    """Render as JSON."""
    return json.dumps(diff_tree, sort_keys=True, indent=2)
