import pytest

from gendiff.generator import generate_diff

# @pytest.fixture
def read_txt(txt_file: str) -> str:
    """Return txt file contents as a string."""
    with open(txt_file, 'r') as input_file:
        text = input_file.read()
    # read adds an additional line feed escape sequence
    # in the end of the text so we have to strip it
    return text.rstrip('\n')


def test_json():
    assert read_txt('./tests/fixtures/expected.txt') == generate_diff('./tests/fixtures/before.json', './tests/fixtures/after.json')

def test_yaml():
    assert read_txt('./tests/fixtures/expected.txt') == generate_diff('./tests/fixtures/before.yaml', './tests/fixtures/after.yaml')
