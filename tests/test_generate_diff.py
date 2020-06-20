"""Test all non-script modules through generate_diff."""

import json
import pathlib

import pytest

from gendiff import format
from gendiff.diff import generate_diff

TESTDIR = pathlib.Path(__file__).parent.absolute()
FIXDIR = TESTDIR / 'fixtures'


def read_txt(txt_file: str) -> str:
    """Return txt file contents as a string."""
    with open(txt_file, 'r') as input_file:
        text = input_file.read()
    # read adds an additional line feed escape sequence
    # in the end of the text so we have to strip it
    return text.rstrip('\n')


@pytest.mark.parametrize(
    'file1,file2,output_format,expected', [
        ('flat_old.json', 'flat_new.json', format.default, 'flat'),
        ('flat_old.yaml', 'flat_new.yaml', format.default, 'flat'),
        ('nested_old.json', 'nested_new.json', format.default, 'nested'),
        ('nested_old.yml', 'nested_new.yml', format.default, 'nested'),
        ('nested_old.json', 'nested_new.json', format.plain, 'plain'),
        ('nested_old.yml', 'nested_new.yml', format.plain, 'plain'),
    ],
)
def test_nonjson_output(file1, file2, output_format, expected):
    assert generate_diff(
        FIXDIR / file1,
        FIXDIR / file2,
        output_format=output_format,
    ) == read_txt(FIXDIR / 'expected_{0}.txt'.format(expected))


@pytest.mark.parametrize(
    'file1,file2', [
        ('nested_old.json', 'nested_new.json'),
        ('nested_old.yml', 'nested_new.yml'),
    ],
)
def test_json_output(file1, file2):
    with open(FIXDIR / 'expected_nested.json', 'r') as expected:
        expected_data = json.load(expected)
    generate_diff_output = generate_diff(
        FIXDIR / file1,
        FIXDIR / file2,
        output_format=format.json,
    )
    assert json.loads(generate_diff_output) == expected_data


def test_single_value_json():
    with pytest.raises(Exception) as exception:
        assert generate_diff(
            FIXDIR / 'single_value_old.json',
            FIXDIR / 'single_value_new.json',
            output_format=format.plain,
        ) == read_txt('./tests/fixtures/expected_plain.txt')
        assert str(exception.value) == (
            'Unsupported .json structure: not a configuration file.'
        )
