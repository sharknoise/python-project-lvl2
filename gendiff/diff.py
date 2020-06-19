"""
Contains generate_diff function and the functions it requires.

generate_diff can be used through the gendiff CL script
or imported into your module.
"""


from gendiff import file, format
from gendiff.ast import build_tree


def generate_diff(
    path_to_file1: str, path_to_file2: str, output_format=format.default,
) -> str:
    """
    Show how one settings file differs from another.

    Args:
        output_format: function formatting the output string:
            format.default
            format.json
            format.plain
            notice that default and plain formats show both the
            different and unchanged properties; plain only renders
            the difference
        path_to_file1: relative or absolute including the filename
        path_to_file2: relative or absolute including the filename

    Returns:
        difference between files as a multiline string
    """
    file1 = file.get_data(path_to_file1)
    file2 = file.get_data(path_to_file2)

    return output_format(build_tree(file1, file2))
