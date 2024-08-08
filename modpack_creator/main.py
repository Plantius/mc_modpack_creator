# Different project selector
# Load project
# Project consist of Name, Build Date, MC Version, Mod Loader, Pack Version, Mod List: Dependencies, Client only, Server only, mod updater
# Compatability check
# Delete project
# Edit project
# Create project

import requests
r = requests.get('https://staging-api.modrinth.com/v2/search?query=sodium')
data = r.json()
print(data)