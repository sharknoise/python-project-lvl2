"""Test the functions from generator.py."""

from gendiff.generator import generate_diff


def read_txt(txt_file: str) -> str:
    """Return txt file contents as a string."""
    with open(txt_file, 'r') as input_file:
        text = input_file.read()
    # read adds an additional line feed escape sequence
    # in the end of the text so we have to strip it
    return text.rstrip('\n')


def test_json_flat():
    assert generate_diff(
        './tests/fixtures/before_flat.json',
        './tests/fixtures/after_flat.json',
    ) == read_txt('./tests/fixtures/expected_flat.txt')


def test_yaml_flat():
    assert generate_diff(
        './tests/fixtures/before_flat.yaml',
        './tests/fixtures/after_flat.yaml',
    ) == read_txt('./tests/fixtures/expected_flat.txt')


def test_json():
    assert generate_diff(
        './tests/fixtures/before.json',
        './tests/fixtures/after.json',
    ) == read_txt('./tests/fixtures/expected.txt')


def test_yaml():
    assert generate_diff(
        './tests/fixtures/before.yaml',
        './tests/fixtures/after.yaml',
    ) == read_txt('./tests/fixtures/expected.txt')
