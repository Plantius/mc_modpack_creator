import argparse

def parse_arguments() -> argparse.Namespace:
    """Parses CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--open_project", required=False, type=str, help="enter name of project file to load")
    return parser.parse_args()
