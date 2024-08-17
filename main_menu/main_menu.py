import standard as std
from modpack_creator import Modrinth
from simple_term_menu import TerminalMenu
from main_menu import options as opt

OPT_PROJECT = [["load_project", "Load project"], ["create_project", "Create project"], 
               ["save_project", "Save project"]]
OPT_MODPACK = [["add_mods", "Add mod(s)"], ["remove_mods", "Remove mod(s)"]]
OPT_CONFIG = [["change_project_name", "Change project name"], ["change_project_version", "Change project version"], 
              ["change_project_loader", "Change mod loader"], ["change_project_version", "Change Minecraft version"]]
OPT_MISC = {"config": [[None, "Change project settings"]], "exit": [["exit_program", "Exit menu"]]}

def get_options_func(opt: list) -> list:
    return [x[0] for x in opt]

def get_options_name(opt: list) -> list:
    return [x[1] for x in opt]


# TODO Add functionalities, make use of functions and change option layout
class menu:
    project: Modrinth.project

    def __init__(self, project: Modrinth.project) -> None:
        self.project = project
    
    def create_config(self, title="A Menu", menu_entries=["Exit"], clear_screen=True, multi_select=False, show_multi_select_hint=False) -> dict:
        return {"title": title, "menu_entries": menu_entries, "clear_screen": clear_screen, "multi_select": multi_select, "show_multi_select_hint": show_multi_select_hint}


    def get_options(self, flags: dict) -> list:
        options = []
        if flags["config"]:
            options += get_options_name(OPT_CONFIG)
        else:
            if flags["loaded"]:
                options += get_options_name(OPT_PROJECT)
                options += get_options_name(OPT_MODPACK)
            else:
                options += get_options_name(OPT_PROJECT)
            options += get_options_name(OPT_MISC["config"])

        return options + get_options_name(OPT_MISC["exit"])    
            

    # TODO Add generalization of common functions
    def main_menu(self) -> None:
        main_flags = {"loaded": self.project.loaded, "config": False}
        config_flags = {"loaded": self.project.loaded, "config": True}
        main_menu_config = self.create_config("Load and edit or create a new project.", 
                                              self.get_options(main_flags),
                                              clear_screen=False)
        sub_menu_config = {"config_menu": self.create_config("Edit the current project's settings.", 
                                                       self.get_options(config_flags),
                                                       clear_screen=False)}

        main_menu = TerminalMenu(**main_menu_config)
        config_menu = TerminalMenu(**sub_menu_config["config_menu"])
        print(std.get_functions(opt))
        while True:
            main_index = main_menu.show()
            if self.get_options(main_flags)[main_index] in get_options_name(OPT_MISC["config"]):
                while True:
                    edit_index = config_menu.show()

                    if sub_menu_config["config_menu"]["menu_entries"][edit_index] in get_options_name(OPT_MISC["exit"]) or edit_index is None:
                        break

            elif main_menu_config["menu_entries"][main_index] in get_options_name(OPT_PROJECT)[0]: # Load project
                func = getattr(opt, get_options_func(OPT_PROJECT)[0])
                if func():
                    print("SUCCES LOAD")
            elif main_menu_config["menu_entries"][main_index] in get_options_name(OPT_PROJECT)[1]: # Create project
                func = getattr(opt, get_options_func(OPT_PROJECT)[1])
                if func():
                    print("SUCCES CREATE")
            elif main_menu_config["menu_entries"][main_index] in get_options_name(OPT_PROJECT)[2]: # Save project
                func = getattr(opt, get_options_func(OPT_PROJECT)[2])
                if func():
                    print("SUCCES SAVE")
                                                                              
            elif main_menu_config["menu_entries"][main_index] in get_options_name(OPT_MISC["exit"]) or main_index is None: # Exit
                func = getattr(opt, get_options_func(OPT_MISC["exit"])[0])
                if func(self.project):
                    print("SUCCES EXIT")
                    break
        
    
        