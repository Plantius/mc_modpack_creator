import time
from modpack import project
from args_parser import args_parser as args
from menu import main_menu

tests = 5

def main():
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
        menu.display()
    start_time = time.time()
    for i in range(tests):
        ids = [id.project_id for id in p.modpack.mod_data]
        m = p.fetch_mods_by_ids(ids)
    end_time = time.time()
    print(f"Avg time taken for fetch_mods_by_ids: {(end_time - start_time)/tests:.4f} seconds")


if __name__ == "__main__":
    main()