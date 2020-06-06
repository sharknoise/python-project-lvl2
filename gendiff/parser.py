"""Functions to parse the contents of json or yaml files."""

import json
import os

import yaml

JSON = '.json'
YAML = '.yaml'
YML = '.yml'
SUPPORTED_FORMATS = JSON, YAML, YML


def get_data(path_to_file: str) -> dict:
    """Return the contents os a json or yaml file as a dict."""
    file_format = os.path.splitext(path_to_file)[1]
    if file_format not in SUPPORTED_FORMATS:
        raise Exception(('Unsupported input format: {0}'.format(file_format)))
    return parse_data(file_format, path_to_file)


def parse_data(file_format: str, path_to_file: str) -> dict:
    """Choose a loader depending on file extension."""
    with open(path_to_file, 'r') as parsed_file:
        if file_format == JSON:
            return json.load(parsed_file)
        elif file_format in {YAML, YML}:
            return yaml.safe_load(parsed_file)
