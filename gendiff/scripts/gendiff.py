"""A CLI utility that shows differences in configuration files."""


import argparse

from gendiff.generator import generate_diff

DEFAULT_OUTPUT_FORMAT = 'jsonlike'


def main():
    """Run the utility in terminal."""
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        metavar='FORMAT_NAME',
        help='set format of the output (jsonlike or plain)',
        default=DEFAULT_OUTPUT_FORMAT,
    )
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file, args.format))


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
