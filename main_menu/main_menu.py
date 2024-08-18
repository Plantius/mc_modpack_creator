import standard as std
from modpack_creator import Modrinth
from simple_term_menu import TerminalMenu
from main_menu import options as opt
from enum import Enum


def get_options_func(opt: list) -> list:
    return [x[0] for x in opt]

def get_options_name(opt: list) -> list:
    return [x[1] for x in opt]

def get_options_id(opt: list) -> list:
    return [x[2] for x in opt]

class Option(Enum):
    PROJECT = 1
    MODPACK = 2
    CONFIG = 3
    SETTINGS = 4
    EXIT = 5


# TODO Add functionalities, make use of functions and change option layout
class menu:
    project: Modrinth.project
    OPT_PROJECT = [["load_project", "Load project", Option.PROJECT], ["create_project", "Create project", Option.PROJECT], 
                ["save_project", "Save project", Option.PROJECT]]
    OPT_MODPACK = [["add_mods", "Add mod(s)", Option.MODPACK], ["remove_mods", "Remove mod(s)", Option.MODPACK]]
    OPT_CONFIG = [["change_project_name", "Change project name", Option.SETTINGS], ["change_project_version", "Change project version", Option.SETTINGS], 
                ["change_project_loader", "Change mod loader", Option.SETTINGS], ["change_mc_version", "Change Minecraft version", Option.SETTINGS]]
    OPT_MISC = {"config": [["get_config_menu", "Change project settings", Option.CONFIG]], "exit": [["exit_program", "Exit menu", Option.EXIT]]}

    def __init__(self, project: Modrinth.project) -> None:
        self.project = project
    
    def create_config(self, title="A Menu", menu_entries=["Exit"], clear_screen=True, multi_select=False, show_multi_select_hint=False) -> dict:
        return {"title": title, "menu_entries": menu_entries, "clear_screen": clear_screen, "multi_select": multi_select, "show_multi_select_hint": show_multi_select_hint}


    def get_options(self, flags: dict) -> list:
        options = []
        if flags["config"]:
            options += self.OPT_CONFIG
        else:
            if flags["loaded"]:
                options += self.OPT_PROJECT
                options += self.OPT_MODPACK
            else:
                options += self.OPT_PROJECT
            options += self.OPT_MISC["config"]

        return options + self.OPT_MISC["exit"]    
            

    # TODO Add generalization of common functions
    def main_menu(self) -> None:
        main_options = self.get_options({"loaded": self.project.loaded, "config": False})
        config_options = self.get_options({"loaded": self.project.loaded, "config": True})

        main_menu_config = self.create_config("Load and edit or create a new project.", 
                                              get_options_name(main_options),
                                              clear_screen=False)
        sub_menu_config = {"config_menu": self.create_config("Edit the current project's settings.", 
                                                       get_options_name(config_options),
                                                       clear_screen=False)}

        main_menu = TerminalMenu(**main_menu_config)
        config_menu = TerminalMenu(**sub_menu_config["config_menu"])
        while True:
            main_index = main_menu.show() # Main menu

            if main_menu_config["menu_entries"][main_index] in get_options_name(main_options)[main_index]: 
                option = get_options_id(main_options)[main_index] # Get  corresponding to option
                func = getattr(opt, get_options_func(main_options)[main_index]) # Get function corresponding to option
                
                if option is Option.CONFIG: # Config submenu
                    while True:
                        config_index = config_menu.show() # Config menu

                        if sub_menu_config["config_menu"]["menu_entries"][config_index] in get_options_name(config_options)[config_index]: 
                            option = get_options_id(config_options)[config_index]
                            func = getattr(opt, get_options_func(config_options)[config_index]) # Get function corresponding to option
    
                            if option is Option.SETTINGS: # Settings
                                if func(self.project):
                                    print(f"SUCCES {sub_menu_config['config_menu']['menu_entries'][config_index]}")
                            elif option is Option.EXIT: # Exit
                                if func(self.project):
                                    print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")
                                    break

                elif option is Option.PROJECT: # Project
                    if func():
                        print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")

                elif option is Option.MODPACK: # Modpack options
                    if func(self.project):
                        print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")

                elif option is Option.EXIT: # Exit
                    if func(self.project):
                        print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")
                        break
            else:
                break
    
        