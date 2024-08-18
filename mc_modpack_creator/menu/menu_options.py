from enum import Enum

class Option(Enum):
    PROJECT = 1
    MODPACK = 2
    CONFIG = 3
    SETTINGS = 4
    EXIT = 5

OPT_PROJECT = [["load_project", "Load project", Option.PROJECT], ["create_project", "Create project", Option.PROJECT], 
                ["save_project", "Save project", Option.PROJECT]]
OPT_MODPACK = [["add_mods", "Add mod(s)", Option.MODPACK], ["remove_mods", "Remove mod(s)", Option.MODPACK]]
OPT_CONFIG = [["change_project_name", "Change project name", Option.SETTINGS], ["change_project_version", "Change project version", Option.SETTINGS], 
            ["change_project_loader", "Change mod loader", Option.SETTINGS], ["change_mc_version", "Change Minecraft version", Option.SETTINGS]]
OPT_MISC = {"config": [["get_config_menu", "Change project settings", Option.CONFIG]], "exit": [["exit_program", "Exit menu", Option.EXIT]]}


def get_options_func(opt: list) -> list:
    return [x[0] for x in opt]

def get_options_name(opt: list) -> list:
    return [x[1] for x in opt]

def get_options_id(opt: list) -> list:
    return [x[2] for x in opt]