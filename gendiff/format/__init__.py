"""Modules that render the difference of settings files."""

from gendiff.format.default import default_format as default
from gendiff.format.json import json_format as json
from gendiff.format.plain import plain_format as plain

FORMATTERS = (JSON, PLAIN, DEFAULT) = (  # noqa: WPS429
    'json', 'plain', 'default',
)
