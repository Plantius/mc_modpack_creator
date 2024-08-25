"""
Configuration constants for the modpack package.

Defines constants for API endpoints, request headers, and default filenames.

Constants
----------
API_BASE : str
    Base URL for the Modrinth API.
HEADERS : dict
    Default HTTP headers with a custom User-Agent.
DEF_FILENAME : str
    Default filename for project files.
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