from modpack import project
from args_parser import args_parser as args
from menu import main_menu

def main():
    # Initialize project and flags
    p = project.Project()

    # Parse command-line arguments
    arguments = args.parse_arguments()
    print(arguments)

    # Load project if specified
    if arguments.open_project:
        p.load_project(arguments.open_project)

    # Initialize and display main menu
    menu = main_menu.Menu(p)
    menu.main_menu()

if __name__ == "__main__":
    main()
