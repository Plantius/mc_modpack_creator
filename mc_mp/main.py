# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

from modpack import project, mod
from args_parser import args_parser as args
from menu import main_menu
import random

def main():
    flags = {"project_loaded": False, "project_saved": False, "project_valid": False, "compatibel": False}

    # Parse arguments
    arguments = args.parse_arguments()
    print(arguments)

    # Project object
    p = project.Project()
    if arguments.open_project is not None:
        p.load_project(arguments.open_project)
    # mod_list = []
    # for i in range(25):
    #     mod_list.append(mod.Mod(f"{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}",
    #                             f"{chr(random.randint(65, 121))*random.randint(1, 5)} {chr(random.randint(65, 121))*random.randint(1, 5)} {chr(random.randint(65, 121))*random.randint(1, 5)}", 
    #                             f"{random.randint(1, 20)}.{random.randint(1, 25)}", 
    #                             f"1.{random.randint(1, 21)}.{random.randint(0, 6)}", 
    #                             random.randint(0, 1), 
    #                             random.randint(0, 1), 
    #                             ["fabric", "forge", "quilt", "neoforge"][random.randint(0, 3)], 
    #                             f"{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}{chr(random.randint(65, 121))}", 
    #                             "Plantius"))
    
    # p.create_project(title="First", description="My first modpack.", build_version="0.1", mc_version="1.21", mod_loader="fabric", mod_list=mod_list)
    # p.save_project("p1.json")
    # p.load_project("p1.json")
    # Main Menu
    menu = main_menu.menu(p)
    menu.main_menu()

if __name__ == "__main__":
    main()