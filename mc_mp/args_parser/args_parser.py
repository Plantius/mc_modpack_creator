from argparse import ArgumentParser, Namespace

def create_parser() -> ArgumentParser:
    """Creates and configures the ArgumentParser for command-line arguments."""
    parser = ArgumentParser(description="Command-line interface for managing project files.")
    
    # Open an existing project
    parser.add_argument(
        "-o", "--open_project",
        type=str,
        required=False,
        help="Specify the project file to load"
    )
    
    # Create a new project
    parser.add_argument(
        "-c", "--create_project",
        type=str,
        required=False,
        help="Specify the name of the new project to create"
    )

    # List all available projects
    parser.add_argument(
        "-l", "--list_projects",
        action="store_true",
        help="List all available projects"
    )
    
    # Delete a project
    parser.add_argument(
        "-d", "--delete_project",
        type=str,
        required=False,
        help="Specify the project file to delete"
    )

    # Add a mod to the current project
    parser.add_argument(
        "-a", "--add_mod",
        type=str,
        required=False,
        help="Specify the mod name to add to the project"
    )

    # Remove a mod from the current project
    parser.add_argument(
        "-r", "--remove_mod",
        type=str,
        required=False,
        help="Specify the mod name to remove from the project"
    )

    # Build the current project
    parser.add_argument(
        "-b", "--build",
        action="store_true",
        help="Build the current project"
    )

    # Export the project configuration
    parser.add_argument(
        "-e", "--export_config",
        type=str,
        required=False,
        help="Export the project configuration to the specified path"
    )

    # Import a project configuration
    parser.add_argument(
        "-i", "--import_config",
        type=str,
        required=False,
        help="Import a project configuration from the specified path"
    )

    # List all mods in the current project
    parser.add_argument(
        "-m", "--list_mods",
        action="store_true",
        help="List all mods in the current project"
    )
    
    # Open the project menu directly
    parser.add_argument(
        "--menu",
        action="store_true",
        help="Open the project menu directly"
    )

    return parser

def parse_arguments() -> Namespace:
    """Parses command-line arguments and returns the result."""
    parser = create_parser()
    return parser.parse_args()
