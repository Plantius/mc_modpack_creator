import standard as std
from modpack_creator import Modrinth
from simple_term_menu import TerminalMenu

OPT_PROJECT = [["load_project", "Load project"], ["create_project", "Create project"], 
               ["save_project", "Save project"]]
OPT_MODPACK = [["add_mods", "Add mod(s)"], ["remove_mods", "Remove mod(s)"]]
OPT_CONFIG = [["change_project_name", "Change project name"], ["change_project_version", "Change project version"], 
              ["change_project_loader", "Change mod loader"], ["change_project_version", "Change Minecraft version"]]
OPT_MISC = {"config": [[None, "Change project settings"]], "exit": [["exit_program", "Exit program"]]}

def get_options_func(opt: list) -> list:
    return [x[0] for x in opt]

def get_options_name(opt: list) -> list:
    return [x[1] for x in opt]


# TODO Add functionalities, make use of functions and change option layout
class menu:
    project: Modrinth.project

    def __init__(self, project: Modrinth.project) -> None:
        self.project = project
    
    def create_config(title="A Menu", options=["Exit"], cursor="> ", cursor_style=("fg_red", "bold"), 
                      style=("bg_red", "fg_yellow"), clear_screen=True, ) -> dict:
        return {"title": title}


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
        main_menu_config = {"sub_menu": {"config_menu": {"options"}}}

        main_flags = {"loaded": self.project.loaded, "config": False}
        config_flags = {"loaded": self.project.loaded, "config": True}

        print(self.get_options(main_flags))
        main_menu = TerminalMenu(self.get_options(main_flags), 
                                 title="Project Creator",
                                 clear_screen=True)
        config_menu = TerminalMenu(self.get_options(config_flags), 
                                 title="Project Editor",
                                 clear_screen=True)
        while True:
            main_index = main_menu.show()
            if self.get_options(main_flags)[main_index] in get_options_name(OPT_MISC["config"]):
                while True:
                    edit_index = config_menu.show()

                    if edit_index >= len(self.get_options(config_flags))-1 or edit_index is None:
                        break
            elif main_index >= len(self.get_options(main_flags))-1 or main_index is None:
                break
        
    
        