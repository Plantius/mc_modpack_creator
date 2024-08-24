from enum import Enum, auto
from typing import List, Dict, Union

class Option(Enum):
    """Enumeration for different types of options in the system."""
    PROJECT = auto()
    ADD_MODS = auto()
    RM_MODS = auto()
    CONFIG = auto()
    SETTINGS = auto()
    EXIT = auto()

# Option Definitions

OPT_PROJECT = [
    ["load_project", "Load project", Option.PROJECT, "Load a project file"],
    ["create_project", "Create project", Option.PROJECT, "Create a new project"],
    ["save_project", "Save project", Option.PROJECT, "Save the current project"]
]

OPT_MODPACK = [
    ["placeholder", "Add mod(s)", Option.ADD_MODS, "Add new mods to the current project"],
    ["remove_mods", "Remove mod(s)", Option.RM_MODS, "Remove mods from the current project"]
]

OPT_ADD_MOD = [
    ["add_mods_input", "Add mod(s)", Option.ADD_MODS, "Add mods using their slug or id"],
    ["search_mods", "Search mod(s)", Option.ADD_MODS, "Search for new mods"]
]

OPT_CONFIG = [
    ["change_project_title", "Change project title", Option.SETTINGS, "Change the current modpack title"],
    ["change_project_description", "Change project description", Option.SETTINGS, "Change the current modpack description"],
    ["change_project_version", "Change project version", Option.SETTINGS, "Change the current modpack build version"],
    ["change_project_loader", "Change mod loader", Option.SETTINGS, "Change the current mod loader"],
    ["change_mc_version", "Change Minecraft version", Option.SETTINGS, "Change the current Minecraft version"]
]

OPT_MISC = {
    "config": [["placeholder", "Change project settings", Option.CONFIG, "Change the current project's settings"]],
    "exit": [["exit_program", "Exit menu", Option.EXIT, "Exit the current menu"]]
}

def extract_option_details(options: list, index: int) -> list:
    """Extracts a specific detail from a list of options."""
    return [option[index] for option in options if option is not None]

def get_options_func(options: list) -> List[str]:
    """Extracts function names from a list of options."""
    return extract_option_details(options, 0)

def get_options_name(options: list) -> List[str]:
    """Extracts descriptive names from a list of options."""
    return extract_option_details(options, 1)

def get_options_id(options: list) -> List[Option]:
    """Extracts option IDs from a list of options."""
    return extract_option_details(options, 2)

def get_options_help(options: list) -> List[str]:
    """Extracts help descriptions from a list of options."""
    return extract_option_details(options, 3)
