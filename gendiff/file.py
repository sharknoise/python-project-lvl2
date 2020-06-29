"""Functions to parse the contents of json or yaml files."""

import json
import os

import yaml

JSON = '.json'
YAML = '.yaml'
YML = '.yml'
SUPPORTED_FORMATS = JSON, YAML, YML


def get_data(path_to_file: str):
    """Return the contents of a json or yaml file."""
    # first value is the name part that we don't need
    _, file_extension = os.path.splitext(path_to_file)
    # we accept extensions typed in uppercase
    file_extension = file_extension.lower()

    if file_extension not in SUPPORTED_FORMATS:
        raise ValueError('Unsupported file format: {0}'.format(file_extension))

    if file_extension == JSON:
        load_data = json.load
    elif file_extension in {YAML, YML}:
        load_data = yaml.safe_load

    with open(path_to_file, 'r') as parsed_file:
        file_contents = load_data(parsed_file)

    if not isinstance(file_contents, dict):
        raise ValueError(
            'Unsupported {0} structure: '.format(file_extension)
            +
            'not a configuration file.',
        )

    return file_contents
