"""
Contains generate_diff function and the functions it requires.

generate_diff can be used through the gendiff CL script
or imported into your module.
"""


from gendiff import parser
from gendiff.ast_builder import build_ast
from gendiff.renderers.jsonlike import jsonlike_render


def generate_diff(path_to_file1: str, path_to_file2: str) -> str:
    """
    Show how two files differ.

    Args:
        path_to_file1: relative or absolute including the filename
        path_to_file2: relative or absolute including the filename

    Returns:
        difference between files as a multiline string
    """
    file1 = parser.get_data(path_to_file1)
    file2 = parser.get_data(path_to_file2)
    return jsonlike_render(build_ast(file1, file2))
