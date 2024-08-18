import standard as std
from modpack_creator import Modrinth
from simple_term_menu import TerminalMenu
from main_menu import menu_functions, menu_options

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
            options += menu_options.OPT_CONFIG
        else:
            if flags["loaded"]:
                options += menu_options.OPT_PROJECT
                options += menu_options.OPT_MODPACK
            else:
                options += menu_options.OPT_PROJECT
            options += menu_options.OPT_MISC["config"]

        return options + menu_options.OPT_MISC["exit"]    
            

    # TODO Add generalization of common functions
    def main_menu(self) -> None:
        main_options = self.get_options({"loaded": self.project.loaded, "config": False})
        config_options = self.get_options({"loaded": self.project.loaded, "config": True})

        main_menu_config = self.create_config("Load and edit or create a new project.", 
                                              menu_options.get_options_name(main_options),
                                              clear_screen=False)
        sub_menu_config = {"config_menu": self.create_config("Edit the current project's settings.", 
                                                       menu_options.get_options_name(config_options),
                                                       clear_screen=False)}

        main_menu = TerminalMenu(**main_menu_config)
        config_menu = TerminalMenu(**sub_menu_config["config_menu"])
        while True:
            main_index = main_menu.show() # Main menu

            if main_menu_config["menu_entries"][main_index] in menu_options.get_options_name(main_options)[main_index]: 
                option = menu_options.get_options_id(main_options)[main_index] # Get  corresponding to option
                func = getattr(menu_functions, menu_options.get_options_func(main_options)[main_index]) # Get function corresponding to option
                
                if option is menu_options.Option.CONFIG: # Config submenu
                    while True:
                        config_index = config_menu.show() # Config menu

                        if sub_menu_config["config_menu"]["menu_entries"][config_index] in menu_options.get_options_name(config_options)[config_index]: 
                            option = menu_options.get_options_id(config_options)[config_index]
                            func = getattr(menu_functions, menu_options.get_options_func(config_options)[config_index]) # Get function corresponding to option
    
                            if option is menu_options.Option.SETTINGS: # Settings
                                if func(self.project):
                                    print(f"SUCCES {sub_menu_config['config_menu']['menu_entries'][config_index]}")
                            elif option is menu_options.Option.EXIT: # Exit
                                if func(self.project):
                                    print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")
                                    break

                elif option is menu_options.Option.PROJECT: # Project
                    if func():
                        print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")

                # TODO Add sub menu to select mods currently in the modpack if delete, or 
                # search for new mods (e.i. search name or enter name, select version etc.) 
                elif option is menu_options.Option.MODPACK: # Modpack options
                    if func(self.project):
                        print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")

                elif option is menu_options.Option.EXIT: # Exit
                    if func(self.project):
                        print(f"SUCCES {main_menu_config['menu_entries'][main_index]}")
                        break
            else:
                break
    
        