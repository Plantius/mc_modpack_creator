"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/main.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from modpack import project
from args_parser import args_parser as args
from menu import main_menu
import asyncio

async def main():
    # Initialize project and flags
    p = project.Project()

    # Parse command-line arguments
    arguments = args.parse_arguments()

    # Handle CLI commands
    if arguments.create_project:
        p.create_project(arguments.create_project)
        p.save_project()
    if arguments.list_projects:
        print(*p.list_projects(), sep='\n')
    if arguments.delete_project:
        p.delete_project(arguments.delete_project)
    if arguments.open_project:
        await p.load_project(arguments.open_project)
    if arguments.list_mods:
        print(*p.list_mods(), sep='\n')

    # Initialize and display main menu
    if arguments.menu_disable:
        menu = main_menu.Menu(p)
        menu.status_bar = menu.get_entry_help
        await menu.display()
    
if __name__ == "__main__":
    asyncio.run(main())