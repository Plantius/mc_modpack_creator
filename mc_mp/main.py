from modpack import project
from args_parser import args_parser as args
from menu import main_menu
import asyncio
import time

tests = 5
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
        p.load_project(arguments.open_project)
    if arguments.list_mods:
        print(*p.list_mods(), sep='\n')

    # Initialize and display main menu
    if arguments.menu_disable:
        menu = main_menu.Menu(p)
        menu.status_bar = menu.get_entry_help
        await menu.display()
    
    start_time = time.perf_counter()
    for i in range(tests):
        ids = [id.project_id for id in p.modpack.mod_data]
        m = await p.fetch_mods_by_ids(ids)
    end_time = time.perf_counter()
    print(f"Time taken for fetch_mods_by_ids: {(end_time - start_time)/tests:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(main())