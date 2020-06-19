"""Test all non-script modules through generate_diff."""

import json
from gendiff import format

from gendiff.diff import generate_diff


def read_txt(txt_file: str) -> str:
    """Return txt file contents as a string."""
    with open(txt_file, 'r') as input_file:
        text = input_file.read()
    # read adds an additional line feed escape sequence
    # in the end of the text so we have to strip it
    return text.rstrip('\n')


def test_flat_json():
    assert generate_diff(
        './tests/fixtures/flat_old.json',
        './tests/fixtures/flat_new.json',
    ) == read_txt('./tests/fixtures/expected_flat.txt')


def test_flat_yaml():
    assert generate_diff(
        './tests/fixtures/flat_old.yaml',
        './tests/fixtures/flat_new.yaml',
    ) == read_txt('./tests/fixtures/expected_flat.txt')


def test_json():
    assert generate_diff(
        './tests/fixtures/nested_old.json',
        './tests/fixtures/nested_new.json',
    ) == read_txt('./tests/fixtures/expected.txt')


def test_yml():
    assert generate_diff(
        './tests/fixtures/nested_old.yml',
        './tests/fixtures/nested_new.yml',
    ) == read_txt('./tests/fixtures/expected.txt')


def test_json_as_plain():
    assert generate_diff(
        './tests/fixtures/nested_old.json',
        './tests/fixtures/nested_new.json',
        output_format=format.plain,
    ) == read_txt('./tests/fixtures/expected_plain.txt')


def test_yml_as_plain():
    assert generate_diff(
        './tests/fixtures/nested_old.yml',
        './tests/fixtures/nested_new.yml',
        output_format=format.plain,
    ) == read_txt('./tests/fixtures/expected_plain.txt')


def test_json_as_json_via_parser():
    with open('./tests/fixtures/expected.json', 'r') as expected:
        expected_data = json.load(expected)
    generate_diff_output = generate_diff(
        './tests/fixtures/nested_old.json',
        './tests/fixtures/nested_new.json',
        output_format=format.json,
    )
    assert json.loads(generate_diff_output) == expected_data


def test_yml_as_json_via_parser():
    with open('./tests/fixtures/expected.json', 'r') as expected:
        expected_data = json.load(expected)
    generate_diff_output = generate_diff(
        './tests/fixtures/nested_old.yml',
        './tests/fixtures/nested_new.yml',
        output_format=format.json,
    )
    assert json.loads(generate_diff_output) == expected_data
