"""A CLI utility finding the differences in configuration files."""


import argparse
from gendiff.generator import generate_diff


def main():
    """Run the utility in terminal."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        metavar='FORMAT',
        help='set format of the output',
    )
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
