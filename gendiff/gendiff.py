"""A CLI utility finding the differences in configuration files."""


import argparse


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
    parser.parse_args()


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
