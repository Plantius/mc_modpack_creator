"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/args_parser/args_parser.py
Last Edited: 2024-09-07

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from argparse import ArgumentParser, Namespace

def create_parser() -> ArgumentParser:
    """Creates and configures the ArgumentParser for command-line arguments."""
    parser = ArgumentParser(description="Command-line interface for managing project files.")
    
    # Open an existing project
    parser.add_argument(
        "-o",
        dest="load_project",
        type=str,
        required=False,
        help="Specify the project file to load"
    )
    
    # Create a new project
    parser.add_argument(
        "-c",
        dest="create_project",
        type=str,
        required=False,
        help="Specify the name of the new project to create"
    )

    # List all available projects
    parser.add_argument(
        "-l",
        dest="list_project",
        action="store_true",
        help="List all available projects"
    )
    
    # Delete a project
    parser.add_argument(
        "-d",
        dest="delete_project",
        type=str,
        required=False,
        help="Specify the project file to delete"
    )

    # List all mods in the current project
    parser.add_argument(
        "-m",
        dest="list_mods",
        action="store_true",
        help="List all mods in the current project"
    )
    
    # Load a specific databse
    parser.add_argument(
        "-s",
        dest="sqlite_database",
        type=str,
        required=False,
        help="Specify the database to load"
    )
    
    # Choose which UI to use
    parser.add_argument(
        "--ui",
        dest="ui",
        type=str,
        help="User interface for Minecraft Modpack Creator. Options: none, cli, web (Default cli)"
    )
    
    # Enable debug mode
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Enables debug mode to display additional information."
    )

    return parser

def parse_arguments() -> Namespace:
    """Parses command-line arguments and returns the result."""
    parser = create_parser()
    return parser.parse_args()
