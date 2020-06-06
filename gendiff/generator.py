"""
Contains generate_diff function and the functions it requires.

generate_diff can be used through the gendiff CL script
or imported into your module.
"""


from gendiff import parser
from gendiff.ast_builder import build_ast
from gendiff.renderers.jsonlike import jsonlike_render
from gendiff.renderers.plain import plain_render


def generate_diff(path_to_file1: str,
                  path_to_file2: str,
                  format='jsonlike') -> str:
    """
    Show how one settings file differs from another.

    Args:
        format: format of the output string;
            notice that the 'jsonlike' format shows all unchanged
            settings in addition to differences
        path_to_file1: relative or absolute including the filename
        path_to_file2: relative or absolute including the filename

    Returns:
        difference between files as a multiline string
    """
    file1 = parser.get_data(path_to_file1)
    file2 = parser.get_data(path_to_file2)
    if format == 'jsonlike':
        return jsonlike_render(build_ast(file1, file2))
    elif format == 'plain':
        return plain_render(build_ast(file1, file2))
    else:
        return (
            'Unable to render the difference. '
            +
            'Only "jsonlike" and "plain" output formats supported.'
        )
