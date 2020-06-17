"""Functions that render as JSON."""

import json


def json_render(ast):
    """Render as JSON."""
    return json.dumps(ast, sort_keys=True, indent=2)
