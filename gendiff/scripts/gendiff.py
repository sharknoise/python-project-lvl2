"""A CLI utility that shows differences in configuration files."""

from gendiff.cli import parser
from gendiff.diff import generate_diff


def main():
    """Run the utility in terminal."""
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file, args.format))


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
