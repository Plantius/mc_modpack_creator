# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

import requests, DateTime
import Modpack, Mod

r = requests.get('https://staging-api.modrinth.com/v2/search?query=sodium')
data = r.json()
print(data)
mod_list = [Mod.mod("Mod", "0.1", "1.20.1", "Client", "Fabric", "https://google.com", "Plantius")]
mp = Modpack.modpack("First", DateTime.DateTime("08-08-2024"), "0.1", "1.20.1", "Fabric", mod_list)