"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/main.py
Last Edited: 2024-09-10

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from mc_mp.modpack.project import Project
from mc_mp.args_parser import args_parser
from mc_mp.menu import main_menu
import asyncio
import mc_mp.standard as std
from web_app.app import create_app

async def main():
    args = args_parser.parse_arguments()
    # Initialize project and flags
    if args.sqlite_database:
        p = Project(args.sqlite_database)
    else :
        p = Project()

    # Parse command-line arguments

    # Handle CLI commands
    if args.debug:
        std.set_debug_flag(args.debug)
    if args.create_project:
        p.create_project(args.create_project)
        p.save_project()
    if args.list_project:
        print(*p.list_projects(), sep='\n')
    if args.load_project:
        await p.load_project(args.load_project)
    if args.list_mods:
        print(*p.list_mods(), sep='\n')
    if args.delete_project:
        p.delete_project(args.delete_project)
        
    # Initialize and display ui
    if args.ui and args.ui == "cli":
        menu = main_menu.Menu(p)
        menu.status_bar = menu.get_entry_help
        await menu.display()
    elif args.ui and args.ui == "web":
        app = create_app(project=p)
        app.run(debug=args.debug if args.debug else False)
    elif args.ui and args.ui == "none":
        pass 
    else:
        menu = main_menu.Menu(p)
        menu.status_bar = menu.get_entry_help
        await menu.display()
    
if __name__ == "__main__":
    asyncio.run(main())