import sys, argparse

def parse_arguments() -> argparse.Namespace:
    """Parses CLI arguments"""
    args = sys.argv
    parser = argparse.ArgumentParser(args[0], 
                                     f"{args[0]}: [--save_project] [-f filename]")
    parser.add_argument("-s", "--save_project", action="store_true", help="save the current project")
    parser.add_argument("-f", "--filename", default="project_1.json", required=False, type=str, help="enter name of project file")
    return parser.parse_args()
