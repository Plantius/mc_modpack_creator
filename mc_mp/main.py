from modpack import project
from args_parser import args_parser as args
from menu import main_menu

def main():
    # Initialize project and flags
    p = project.Project()

    # Parse command-line arguments
    arguments = args.parse_arguments()
    print(arguments)

    # Handle CLI commands
    if arguments.create_project:
        p.create_project(arguments.create_project)
        p.save_project()
    if arguments.list_projects:
        print(p.list_projects())
    if arguments.delete_project:
        p.delete_project(arguments.delete_project)
    if arguments.add_mod:
        p.add_mod(arguments.add_mod)
    if arguments.remove_mod:
        p.remove_mod(arguments.remove_mod)
    if arguments.list_mods:
        print(p.list_mods())
    if arguments.open_project:
        p.load_project(arguments.open_project)

    # Initialize and display main menu
    if arguments.menu:
        menu = main_menu.Menu(p)
        menu.main_menu()

if __name__ == "__main__":
    main()