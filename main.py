# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

from modpack_creator import Modrinth, Mod
import sys

# args = sys.argv


# mod_list = [Mod.mod("Mod", "0.1", "1.20.1", False, True, "Fabric", "AAA", "Plantius"),
#             Mod.mod("Mod", "0.1", "1.20.1", True, True, "Fabric", "BBB", "Plantius")]
# p = Modrinth.project("First", build_version="0.1", mc_version="1.19", mod_loader="forge", mod_list=mod_list)

p = Modrinth.project()
# p.mp.load_project("p1")
# p.mp.save_project(args[1])

# print(p.search_project("graves"))
# print(p.search_project("apple", [["categories:fabric"], ["versions:1.21"]]))
# print(p.list_versions("sodium", ["fabric"], ["1.21"]))
print(p.get_version("RncWhTxD"))
# print(p.get_project("sodium"))

# # mp = Modpack.modpack("First", DateTime("08-08-2024"), "0.1", "1.20.1", "Fabric", mod_list)
# mp = Modpack.modpack()
