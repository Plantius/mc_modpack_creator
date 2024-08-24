from enum import Enum

class Option(Enum):
    PROJECT = 1
    ADD_MODS = 2
    RM_MODS = 3
    CONFIG = 4
    SETTINGS = 5
    EXIT = 6


# Function name, name, option id, help
OPT_PROJECT = [["load_project", "Load project", Option.PROJECT, "Load a project file"], 
               ["create_project", "Create project", Option.PROJECT, "Create a new project"], 
               ["save_project", "Save project", Option.PROJECT, "Save the current project"]]

OPT_MODPACK = [["placeholder", "Add mod(s)", Option.ADD_MODS, "Add new mods to the current project"], 
               ["remove_mods", "Remove mod(s)", Option.RM_MODS, "Remove mods from the current project"]]

OPT_ADD_MOD = [["add_mods_input", "Add mod(s)", Option.ADD_MODS, "Add mods using their slug or id"],
               ["search_mods", "Search mod(s)", Option.ADD_MODS, "Search for new mods"]]

OPT_CONFIG = [["change_project_name", "Change project name", Option.SETTINGS, "Change the current modpack title"], 
              ["change_project_version", "Change project version", Option.SETTINGS, "Change the current modpack build version"], 
              ["change_project_loader", "Change mod loader", Option.SETTINGS, "Change the current mod loader"], 
              ["change_mc_version", "Change Minecraft version", Option.SETTINGS, "Change the current minecraft version"],
              ["allow_alpha_beta", "Allow alpha or beta mods?", Option.SETTINGS, "Allow mods with version alpha or beta?"]]

OPT_MISC = {"config": [["placeholder", "Change project settings", Option.CONFIG, "Change the current project' settings"]], 
            "exit": [["exit_program", "Exit menu", Option.EXIT, "Exit the current menu"]]}


def get_options_func(opt: list) -> list:
    return [x[0] if x is not None else None for x in opt]

def get_options_name(opt: list) -> list:
    return [x[1] if x is not None else None for x in opt]

def get_options_id(opt: list) -> list:
    return [x[2] if x is not None else None for x in opt]

def get_options_help(opt: list) -> list:
    return [x[3] if x is not None else None for x in opt]