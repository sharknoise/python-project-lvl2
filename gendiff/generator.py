"""
Contains generate_diff function and private functions it requires.

generate_diff can be used by the gendiff CL script
or imported into your module.
"""


import json


def generate_diff(path_to_file1: str, path_to_file2: str) -> str:
    """
    Show how two files differ.

    Args:
        path_to_file1: relative or absolute including the filename
        path_to_file2: relative or absolute including the filename

    Returns:
        difference between files as a multiline string
    """
    file1 = read_json(path_to_file1)
    file2 = read_json(path_to_file2)
    diff_table = create_diff_table(file1, file2)
    return diff_table_to_str(diff_table)


def read_json(path_to_file: str) -> dict:
    """Get the contents of a json file."""
    with open(path_to_file, 'r') as json_file:
        json_contents = json.load(json_file)
    return json_contents


def create_diff_table(dict1: dict, dict2: dict) -> dict:
    """
    Create a table with values from both dictionaries for comparison.

    Args:
        dict1: first dictionary
        dict2: second dictionary

    Returns:
        a new dictionary with the following structure
        key: (value from dict1, value from dict2)
        if a key didn't exist in one of the dicts, the value will be None
    """
    all_keys = set(dict1.keys()) | set(dict2.keys())
    diff_table = {}
    for key in all_keys:
        diff_table[key] = (dict1.get(key), dict2.get(key))
    return diff_table


# ignore WPS231 as the comlpexity is readable here
def diff_table_to_str(diff_table: dict) -> str:  # noqa: WPS231
    """
    Transform a comparison table into a multiline string.

    Args:
        diff_table: a table created by create_diff_table

    Returns:
        a multiline string where:
        all new values are marked with a +
        all changed or deleted values are marked with a -
        all unchanged values are shown without any sign
    """
    lines = ['{']
    for key, value_pair in sorted(diff_table.items()):
        # WPS forbids unpacking in the for statement
        old_value, new_value = value_pair
        if old_value is None and new_value is not None:
            lines.append(create_line_with_sign('+', key, new_value))
        elif old_value is not None and new_value is None:
            lines.append(create_line_with_sign('-', key, old_value))
        elif old_value == new_value:
            lines.append(create_line_with_sign(' ', key, old_value))
        else:
            lines.append(create_line_with_sign('-', key, old_value))
            lines.append(create_line_with_sign('+', key, new_value))
    lines.append('}')
    return '\n'.join(lines)


def create_line_with_sign(sign: str, key, value) -> str:  # noqa: WPS110
    """Return arguments as a string with a sign in the beginning."""
    return '{0} {1}: {2}'.format(sign, str(key), str(value))
