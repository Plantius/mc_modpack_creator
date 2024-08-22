from enum import Enum

class Option(Enum):
    PROJECT = 1
    ADD_MODS = 2
    RM_MODS = 3
    CONFIG = 4
    SETTINGS = 5
    EXIT = 6


# Function name, name, option id
OPT_PROJECT = [["load_project", "Load project", Option.PROJECT], 
               ["create_project", "Create project", Option.PROJECT], 
               ["save_project", "Save project", Option.PROJECT]]

OPT_MODPACK = [["add_mods", "Add mod(s)", Option.ADD_MODS], 
               ["remove_mods", "Remove mod(s)", Option.RM_MODS]]

OPT_ADD_MOD = [["search_mods", "Search mod(s)", Option.ADD_MODS],
               ["add_mods_from_file", "Add mod(s) from file", Option.ADD_MODS]]

OPT_CONFIG = [["change_project_name", "Change project name", Option.SETTINGS], 
              ["change_project_version", "Change project version", Option.SETTINGS], 
              ["change_project_loader", "Change mod loader", Option.SETTINGS], 
              ["change_mc_version", "Change Minecraft version", Option.SETTINGS]]

OPT_MISC = {"config": [["get_config_menu", "Change project settings", Option.CONFIG]], 
            "exit": [["exit_program", "Exit menu", Option.EXIT]]}


def get_options_func(opt: list) -> list:
    return [x[0] for x in opt]

def get_options_name(opt: list) -> list:
    return [x[1] for x in opt]

def get_options_id(opt: list) -> list:
    return [x[2] for x in opt]