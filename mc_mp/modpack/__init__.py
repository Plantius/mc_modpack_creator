"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/__init__.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""

# Base URL for Modrinth API
API_BASE = 'https://api.modrinth.com/v2'

# Default request headers
HEADERS = {
    'User-Agent': 'Plantius/mc_modpack_creator'
}

# Default project filename
DEF_FILENAME = "project_1.json"

# Indicates acceptance of a prompt
ACCEPT = 'y'

PROJECT_DIR = "./mp"

MAX_WORKERS = 8

# Modrinth Modpack Formats
FORMAT_VERSION = 1
GAME = "minecraft"
MOD_PATH = 'mods/'
MR_INDEX = "modrinth.index.json"
MRPACK = "mrpack"

# Loader versions
FABRIC_V = "0.16.0"

