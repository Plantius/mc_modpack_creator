# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

from modpack_creator import Modrinth, Modpack, Mod

p = Modrinth.project()

print(p.search_project("indium", ))

mod_list = [Mod.mod("Mod", "0.1", "1.20.1", False, True, "Fabric", "https://google.com", "Plantius"),
            Mod.mod("Mod", "0.1", "1.20.1", True, True, "Fabric", "https://google.com", "Plantius")]
# mp = Modpack.modpack("First", DateTime("08-08-2024"), "0.1", "1.20.1", "Fabric", mod_list)
mp = Modpack.modpack()
