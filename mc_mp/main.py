from modpack import project
from args_parser import args_parser as args
from menu import main_menu

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
        menu.update_entries()
        menu.display()
        

if __name__ == "__main__":
    main()