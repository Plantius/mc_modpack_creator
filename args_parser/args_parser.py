import sys, argparse
from . import constants


def parse_arguments():
    """Parses CLI arguments"""
    args = sys.argv
    parser = argparse.ArgumentParser("Modpack creator", 
                                     f"{args[0]}: [-f filename]")
    for name, pos, default, type, req, help in constants.ARGUMENTS:
        parser.add_argument(name, pos, default=default, type=type, required=req, help=help)
    args = parser.parse_args()
