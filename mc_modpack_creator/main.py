# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

from modpack import project
from args_parser import args_parser as args
from menu import main_menu


def main():
    flags = {"project_loaded": False, "project_saved": False, "project_valid": False, "compatibel": False}

    # Parse arguments
    arguments = args.parse_arguments()
    print(arguments)

    # Project object
    p = project.Project()
    # mod_list = [Mod.mod("Mod", "0.1", "1.20.1", False, True, "Fabric", "AAA", "Plantius"),
    #             Mod.mod("Mod", "0.1", "1.20.1", True, True, "Fabric", "BBB", "Plantius")]
    # p.create_project("First", build_version="0.1", mc_version="1.19", mod_loader="forge", mod_list=mod_list)
    # p.save_project("p1")
    p.load_project("p1.json")
    
    # Main Menu
    menu = main_menu.menu(p)
    menu.main_menu()

if __name__ == "__main__":
    main()