from enum import Enum, auto
from typing import List, Dict, Union

class Option(Enum):
    """Enumeration for different types of options in the system."""
    PROJECT = auto()
    ADD_MODS = auto()
    RM_MODS = auto()
    LIST_MODS = auto()
    UPDATE_MODS = auto()
    CONFIG = auto()
    SETTINGS = auto()
    EXIT = auto()

# Option Definitions
OPT_PROJECT = [
    ["load_project_menu", "Load project", Option.PROJECT, "Load a project file"],
    ["create_project_menu", "Create project", Option.PROJECT, "Create a new project"],
    ["save_project_menu", "Save project", Option.PROJECT, "Save the current project"]
]

OPT_MODPACK = [
    ["add_mods_menu", "Add mod(s)", Option.ADD_MODS, "Add new mods to the current project"],
    ["rm_mods_menu", "Remove mod(s)", Option.RM_MODS, "Remove mods from the current project"],
    ["list_mods_menu", "List mod(s)", Option.LIST_MODS, "List all mods in the current project"],
    ["update_mods_menu", "Update mods", Option.UPDATE_MODS, "Update all mods in the current project"]
]

OPT_ADD_MOD = [
    ["add_mods_id_menu", "Add mod(s) by id", Option.ADD_MODS, "Add mods using their slug or id"],
    ["add_mods_file_menu", "Add mod(s) by file", Option.ADD_MODS, "Add mods using file"],
    ["search_mods_menu", "Search mod(s)", Option.ADD_MODS, "Search for new mods"]
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

def get_options(options: list) -> Dict[str, List[Union[str, Option]]]:
    """Extracts all relevant details from a list of options."""
    return {
        'functions': extract_option_details(options, 0),
        'names': extract_option_details(options, 1),
        'ids': extract_option_details(options, 2),
        'help': extract_option_details(options, 3)
    }
