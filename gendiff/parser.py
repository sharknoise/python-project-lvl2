"""Functions to parse the contents of json or yaml files."""

import json
import os
from typing import Any, Dict

import yaml

JSON = '.json'
YAML = '.yaml'
YML = '.yml'
SUPPORTED_FORMATS = JSON, YAML, YML


def get_data(path_to_file: str) -> Dict[str, Any]:
    """Return the contents of a json or yaml file as a dict."""
    file_extension = os.path.splitext(path_to_file)[1]
    if file_extension not in SUPPORTED_FORMATS:
        raise Exception('Unsupported file format: {0}'.format(file_extension))
    return parse_file(file_extension, path_to_file)


def parse_file(file_extension: str, path_to_file: str) -> Dict[str, Any]:
    """Load file contents with the appropriate loader."""
    with open(path_to_file, 'r') as parsed_file:
        if file_extension == JSON:
            return json.load(parsed_file)
        elif file_extension in {YAML, YML}:
            return yaml.safe_load(parsed_file)
