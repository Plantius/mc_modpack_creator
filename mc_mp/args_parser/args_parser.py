"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/args_parser/args_parser.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
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

    # List all mods in the current project
    parser.add_argument(
        "-m", "--list_mods",
        action="store_true",
        help="List all mods in the current project"
    )
    
    # Dont launch the menu when set
    parser.add_argument(
        "--menu_disable",
        action="store_false",
        help="Disable the project menu"
    )

    return parser

def parse_arguments() -> Namespace:
    """Parses command-line arguments and returns the result."""
    parser = create_parser()
    return parser.parse_args()
