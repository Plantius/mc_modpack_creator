from menu import menu_func, menu_options
from modpack import project
from simple_term_menu import TerminalMenu
import standard as std

# TODO Add Mod Update, Mod down/upgrade, Mod Version down/upgrade
class menu:
    p: project.Project
    
    def __init__(self, p: project.Project) -> None:
        self.p = p
    
    def create_config(self, title="A Menu", menu_entries=["Exit"], cursor_index=0, 
                      clear_screen=True, multi_select=False, show_multi_select_hint=False,
                      status_bar="No project loaded") -> dict:
        return {"title": title, "menu_entries": menu_entries, "cursor_index": cursor_index, 
                "clear_screen": clear_screen, "multi_select": multi_select, "show_multi_select_hint": show_multi_select_hint,
                "status_bar": status_bar}


    def get_options(self, flags: dict) -> list:
        options = []

        if flags["config"]:
            options += menu_options.OPT_CONFIG
        elif not flags["mod"]:
            if flags["loaded"]:
                options += menu_options.OPT_PROJECT
                options += menu_options.OPT_MODPACK
                options += menu_options.OPT_MISC["config"]
            else:
                options += menu_options.OPT_PROJECT
        else:
            options += menu_options.OPT_ADD_MOD

        return options + menu_options.OPT_MISC["exit"]    
    
    def get_project_info(self) -> str:
        return f"{self.p.mp.title}: {self.p.mp.description} | Version {self.p.mp.build_version} | {self.p.mp.build_date} | {self.p.mp.mc_version} | {self.p.mp.mod_loader} | {len(self.p.mp.mod_list)} mods" 
    
    def update_menu(self, config) -> TerminalMenu:
        return TerminalMenu(**config)

    def config_menu(self, config_options) -> None:
        config_index = 0
        while True:
            if self.p.metadata["loaded"]:
                status = self.get_project_info()
            config_menu = TerminalMenu(**self.create_config("Edit project settings.", 
                                            menu_options.get_options_name(config_options),
                                            cursor_index=config_index,
                                            status_bar=status,
                                            clear_screen=False))
            config_index = config_menu.show() # Config menu
            if config_index is None:
                break
        
            option = menu_options.get_options_id(config_options)[config_index]
            func = getattr(menu_func, menu_options.get_options_func(config_options)[config_index]) # Get function corresponding to option

            if option is menu_options.Option.SETTINGS: # Settings
                if not func(self.p):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(config_options)[config_index]}")
            
            elif option is menu_options.Option.EXIT: # Exit
                break
    
    def rm_mod_menu(self, main_options, main_index, func) -> None:
        """Creates a menu containing all mods currently included in the project"""
        while True:
            if self.p.metadata["loaded"]:
                status = self.get_project_info() 
            mod_menu = TerminalMenu(**self.create_config("Select which mods to remove.",
                                        self.p.mp.get_mod_list_names(),
                                        multi_select=True,
                                        status_bar=status,
                                        clear_screen=False))
            # Config menu
            mod_index = mod_menu.show() 
            if mod_index is None:
                break

            print(mod_index, mod_menu.chosen_menu_indices)
            if not func(self.p, mod_index):
                print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")
    
    def add_mod_menu(self, mod_options) -> None:
        """Creates a menu with options to add a mod by name/id, search for mods, or return to the previous menu"""
        while True:
            if self.p.metadata["loaded"]:
                status = self.get_project_info() 
            mod_menu = TerminalMenu(**self.create_config("Search for new mods to add to the project.",
                                        menu_options.get_options_name(mod_options),
                                        status_bar=status,
                                        clear_screen=False))
            # Config menu
            mod_index = mod_menu.show() 
            if mod_index is None:
                break

            option = menu_options.get_options_id(mod_options)[mod_index]
            func = getattr(menu_func, menu_options.get_options_func(mod_options)[mod_index]) # Get function corresponding to option
            if option is menu_options.Option.ADD_MODS: # Settings
                if not func(self.p):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(mod_options)[mod_index]}")
            
            elif option is menu_options.Option.EXIT: # Exit
                break


    # TODO Add generalization of common functions
    def main_menu(self) -> None:
        main_index = 0
        status = "No project loaded"
        while True:
            if self.p.metadata["loaded"]:
                status = self.get_project_info()
            main_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": False})
            config_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": True, "mod": False})
            mod_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": True})

            main_menu = TerminalMenu(**self.create_config("Load and edit or create a new project.", 
                                                     menu_options.get_options_name(main_options),
                                                     cursor_index=main_index,
                                                     status_bar=status,
                                                     clear_screen=False))
            # Main menu
            main_index = main_menu.show() 
            if main_index is None:
                func = getattr(menu_func, menu_options.OPT_MISC["exit"][0][0])
                if not func(self.p):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")
                break

            option = menu_options.get_options_id(main_options)[main_index] # Get corresponding to option
            func = getattr(menu_func, menu_options.get_options_func(main_options)[main_index]) # Get function corresponding to option
            
            # Config submenu
            if option is menu_options.Option.CONFIG: 
                self.config_menu(config_options)

            # Project
            elif option is menu_options.Option.PROJECT: 
                if not func(self.p):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")

            # TODO Add sub menu to select mods currently in the modpack if delete, or 
            # search for new mods (e.i. search name or enter name, select version etc.) 

            # Add mods
            elif option is menu_options.Option.ADD_MODS: 
                self.add_mod_menu(mod_options)

            # Remove mods
            elif option is menu_options.Option.RM_MODS: 
                self.rm_mod_menu(main_options, main_index, func)

            # Exit
            elif option is menu_options.Option.EXIT: 
                if not func(self.p):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")
                break
    