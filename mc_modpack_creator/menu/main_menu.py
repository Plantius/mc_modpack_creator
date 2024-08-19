from menu import menu_func, menu_options
from modpack import project
from simple_term_menu import TerminalMenu
import standard as std

# TODO Add functionalities, make use of functions and change option layout
class menu:
    proj: project.Project
    
    def __init__(self, proj: project.Project) -> None:
        self.proj = proj
    
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
        else:
            if flags["loaded"]:
                options += menu_options.OPT_PROJECT
                options += menu_options.OPT_MODPACK
                options += menu_options.OPT_MISC["config"]
            else:
                options += menu_options.OPT_PROJECT
            

        return options + menu_options.OPT_MISC["exit"]    
            
    def update_menu(self, config) -> TerminalMenu:
        return TerminalMenu(**config)


    # TODO Add generalization of common functions
    def main_menu(self) -> None:
        main_index = 0
        config_index = 0
        status = "No project loaded"
        while True:
            std.eprint("MAIN LOOP")
            if self.proj.loaded:
               status = f"{self.proj.mp.name}: {self.proj.mp.description} | {self.proj.mp.build_version} | {self.proj.mp.build_date}" 
            main_options = self.get_options({"loaded": self.proj.loaded, "config": False})
            config_options = self.get_options({"loaded": self.proj.loaded, "config": True})
            main_menu = TerminalMenu(**self.create_config("Load and edit or create a new project.", 
                                                     menu_options.get_options_name(main_options),
                                                     cursor_index=main_index,
                                                     status_bar=status,
                                                     clear_screen=False))
            # Main menu
            main_index = main_menu.show() 
            if main_index is None:
                func = getattr(menu_func, menu_options.OPT_MISC["exit"][0][0])
                if not func(self.proj):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")
                break

            option = menu_options.get_options_id(main_options)[main_index] # Get corresponding to option
            func = getattr(menu_func, menu_options.get_options_func(main_options)[main_index]) # Get function corresponding to option
            
            # Config submenu
            if option is menu_options.Option.CONFIG: 
                while True:
                    std.eprint("CONFIG LOOP")
                    config_menu = TerminalMenu(**self.create_config("Edit project settings.", 
                                                    menu_options.get_options_name(config_options),
                                                    cursor_index=config_index,
                                                    clear_screen=False))
                    config_index = config_menu.show() # Config menu
                    if config_index is None:
                        break
                
                    option = menu_options.get_options_id(config_options)[config_index]
                    func = getattr(menu_func, menu_options.get_options_func(config_options)[config_index]) # Get function corresponding to option

                    if option is menu_options.Option.SETTINGS: # Settings
                        if not func(self.proj):
                            print(f"[ERROR] Could not execute {menu_options.get_options_func(config_options)[config_index]}")
                        self.proj.saved = False
                    elif option is menu_options.Option.EXIT: # Exit
                        break
            # Project
            elif option is menu_options.Option.PROJECT: 
                if not func(self.proj):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")

            # TODO Add sub menu to select mods currently in the modpack if delete, or 
            # search for new mods (e.i. search name or enter name, select version etc.) 

            # Add mods
            elif option is menu_options.Option.ADD_MODS: 
                if not func(self.proj):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")

            # Remove mods
            elif option is menu_options.Option.RM_MODS: 
                while True:
                    std.eprint("MOD LOOP")
                    mod_menu = TerminalMenu(**self.create_config("Select which mods to remove.",
                                                self.proj.mp.get_mod_list_names(),
                                                multi_select=True,
                                                clear_screen=False))
                    # Config menu
                    mod_index = mod_menu.show() 
                    if mod_index is None:
                        break

                    print(mod_index, mod_menu.chosen_menu_indices)
                    if not func(self.proj, mod_index):
                        print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")
                    self.proj.saved = False

            # Exit
            elif option is menu_options.Option.EXIT: 
                if not func(self.proj):
                    print(f"[ERROR] Could not execute {menu_options.get_options_func(main_options)[main_index]}")
                break
    
        