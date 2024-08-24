from argparse import ArgumentParser, Namespace

def create_parser() -> ArgumentParser:
    """Creates and configures the ArgumentParser for command-line arguments."""
    parser = ArgumentParser(description="Command-line interface for managing project files.")
    parser.add_argument(
        "-o", "--open_project",
        type=str,
        required=False,
        help="Specify the project file to load"
    )
    return parser

def parse_arguments() -> Namespace:
    """Parses command-line arguments and returns the result."""
    parser = create_parser()
    return parser.parse_args()
