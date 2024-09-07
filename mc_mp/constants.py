"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/constants.py
Last Edited: 2024-09-07

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
BUF_SIZE = 2 << 15
MAX_WORKERS = 8

SECRET_KEY = b'7rfdYCctHr9xCK2H4i92HLvxN4YzsTty4OrNaAC-bfc='
UNIQUE_ID = "MC_MODPACK_CREATOR_ID"

ALLOWED_CATEGORIES = ["forge", "fabric", "neoforge", "quilt", "liteloader"]

# Base URL for Modrinth API
API_BASE = 'https://api.modrinth.com/v2'
# Default request headers
HEADERS = {
    'User-Agent': 'Plantius/mc_modpack_creator'
}
# Default project filename
DEF_FILENAME = "project_1.json"
DEF_EXT = "modpack"
PROJECT_DIR = "./mp"

# Indicates acceptance of a prompt
ACCEPT = 'y'
QUIT = 'q'


# Modrinth Modpack Formats
FORMAT_VERSION = 1
GAME = "minecraft"
MOD_PATH = 'mods/'
MR_INDEX = "modrinth.index.json"
MRPACK = "mrpack"

# Loader versions
FABRIC_V = "0.16.0"

# Clear screen
CLEAR_SCREEN = False

# Define Open or Close for menu's 
OPEN: bool = True
CLOSE: bool = False