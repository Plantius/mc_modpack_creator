# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

from modpack_creator import Modrinth, Mod
from args_parser import args_parser as args
from main_menu import main_menu as menu

flags = {"project_loaded": False, "project_saved": False, "project_valid": False, "compatibel": False}

# Parse arguments
arguments = args.parse_arguments()
print(arguments)
# Main Menu
# menu.main_menu()


mod_list = [Mod.mod("Mod", "0.1", "1.20.1", False, True, "Fabric", "AAA", "Plantius"),
            Mod.mod("Mod", "0.1", "1.20.1", True, True, "Fabric", "BBB", "Plantius")]
p = Modrinth.project()
p.create_project("First", build_version="0.1", mc_version="1.19", mod_loader="forge", mod_list=mod_list)
p.save_project(arguments.filename)
# p.load_project("p1")
# md = Mod.mod()
# md.load_json(p.mp.mod_list[0])
# print(md.mc_version)

