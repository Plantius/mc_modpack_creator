from menu import menu_func, menu_options as m
from modpack import project
from simple_term_menu import TerminalMenu
import standard as std
import textwrap as tw

class Menu:
    """
    A class to manage and interact with the menu system for a project.

    Attributes
    ----------
    p : project.Project
        An instance of the `Project` class that the menu operates on.

    Methods
    -------
    create_config(title="A Menu", menu_entries=["Exit"], cursor_index=0, 
                  clear_screen=True, multi_select=False, show_multi_select_hint=False,
                  status_bar="No project loaded") -> dict
        Creates a configuration dictionary for a menu.
    
    get_options(flags: dict) -> list
        Returns a list of options based on the provided flags.
    
    get_project_status(entry: str) -> str
        Retrieves the status of a project option based on the provided entry.
    
    get_mod_status(entry: str) -> str
        Retrieves the status of a mod based on the provided entry.
    
    config_menu(config_options: dict) -> None
        Displays a menu for editing project settings.
    
    rm_mod_menu(main_options: dict, main_index: int, func: callable) -> None
        Displays a menu for removing mods from the project.
    
    add_mod_menu(mod_options: dict) -> None
        Displays a menu for adding new mods to the project.
    
    main_menu() -> None
        Displays the main menu and handles user interactions with different options.
    """

    def __init__(self, p: project.Project) -> None:
        """
        Initializes the `Menu` instance with a project.
        """
        self.p = p

    def create_config(self, title="A Menu", menu_entries=["Exit"], cursor_index=0, 
                      clear_screen=True, multi_select=False, show_multi_select_hint=False,
                      status_bar="No project loaded") -> dict:
        """
        Creates a configuration dictionary for a menu.
        """
        return {
            "title": title,
            "menu_entries": menu_entries,
            "cursor_index": cursor_index,
            "clear_screen": clear_screen,
            "multi_select": multi_select,
            "show_multi_select_hint": show_multi_select_hint,
            "status_bar": status_bar
        }

    def get_options(self, flags: dict) -> list:
        """
        Returns a list of options based on the provided flags.
        """
        options = []

        if flags["config"]:
            options.extend(m.OPT_CONFIG)
        elif not flags["mod"]:
            if flags["loaded"]:
                options.extend(m.OPT_PROJECT + m.OPT_MODPACK + m.OPT_MISC["config"])
            else:
                options.extend(m.OPT_PROJECT)
        else:
            options.extend(m.OPT_ADD_MOD)

        return options + [None] + m.OPT_MISC["exit"]

    def get_project_status(self, entry) -> str:
        for lst in [m.OPT_PROJECT, m.OPT_MODPACK, m.OPT_ADD_MOD, m.OPT_CONFIG]:
            i = std.get_index(m.get_options_name(lst), entry)
            if i is not None:
                return m.get_options_help(lst)[i]

        for option in m.OPT_MISC.keys():
            i = std.get_index(m.get_options_name(m.OPT_MISC[option]), entry)
            if i is not None:
                return m.get_options_help(m.OPT_MISC[option])[i]

    def get_mod_status(self, entry: str) -> str:
        """
        Retrieves the status of a mod based on the provided entry.
        """
        index = std.get_index(self.p.mp.get_mod_list_names(), entry)
        if index is not None:
            return f'{entry}: ' + tw.fill(self.p.mp.mod_list[index].description, width=100, fix_sentence_endings=True)
        return entry

    def config_menu(self, config_options: dict) -> None:
        """
        Displays a menu for editing project settings.
        """
        while True:
            config_menu = TerminalMenu(**self.create_config(
                title="Edit project settings.",
                menu_entries=m.get_options_name(config_options),
                status_bar=self.get_project_status
            ))
            config_index = config_menu.show() 
            if config_index is None:
                break

            option = m.get_options_id(config_options)[config_index]
            func = getattr(menu_func, m.get_options_func(config_options)[config_index])

            if option is m.Option.SETTINGS and not func(self.p):
                print(f"[ERROR] Could not execute {m.get_options_func(config_options)[config_index]}")
            elif option is m.Option.EXIT:
                break

    def rm_mod_menu(self, main_options: dict, main_index: int, func: callable) -> None:
        """
        Displays a menu for removing mods from the project.
        """
        while True:
            mod_menu = TerminalMenu(**self.create_config(
                title="Select which mods to remove.",
                menu_entries=self.p.mp.get_mod_list_names(),
                multi_select=True,
                status_bar=self.get_mod_status
            ))
            mod_index = mod_menu.show() 
            if mod_index is None:
                break

            if not func(self.p, mod_index):
                print(f"[ERROR] Could not execute {m.get_options_func(main_options)[main_index]}")

    def add_mod_menu(self, mod_options: dict) -> None:
        """
        Displays a menu for adding new mods to the project.
        """
        while True:
            mod_menu = TerminalMenu(**self.create_config(
                title="Search for new mods to add to the project.",
                menu_entries=m.get_options_name(mod_options),
                status_bar=self.get_project_status
            ))
            mod_index = mod_menu.show() 
            if mod_index is None:
                break

            option = m.get_options_id(mod_options)[mod_index]
            func = getattr(menu_func, m.get_options_func(mod_options)[mod_index])
            if option is m.Option.ADD_MODS and not func(self.p):
                print(f"[ERROR] Could not execute {m.get_options_func(mod_options)[mod_index]}")
            elif option is m.Option.EXIT:
                break

    def main_menu(self) -> None:
        """
        Displays the main menu and handles user interactions with different options.
        """
        cursor_index: int = 0
        while True:
            title = self.get_project_title()
            main_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": False})
            config_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": True, "mod": False})
            mod_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": True})

            main_menu = TerminalMenu(**self.create_config(
                title=title,
                cursor_index=cursor_index,
                menu_entries=m.get_options_name(main_options),
                status_bar=self.get_project_status
            ))
            main_index = main_menu.show()
            if main_index is None:
                func = getattr(menu_func, m.OPT_MISC["exit"][0][0])
                if not func(self.p):
                    print(f"[ERROR] Could not execute exit function")
                break
            cursor_index = main_index
            option = m.get_options_id(main_options)[main_index]
            func = getattr(menu_func, m.get_options_func(main_options)[main_index])

            if option is m.Option.CONFIG:
                self.config_menu(config_options)
            elif option is m.Option.PROJECT:
                if not func(self.p):
                    print(f"[ERROR] Could not execute {m.get_options_func(main_options)[main_index]}")
            elif option is m.Option.ADD_MODS:
                self.add_mod_menu(mod_options)
            elif option is m.Option.RM_MODS:
                self.rm_mod_menu(main_options, main_index, func)
            elif option is m.Option.EXIT:
                if not func(self.p):
                    print(f"[ERROR] Could not execute {m.get_options_func(main_options)[main_index]}")
                break

    def get_project_title(self) -> str:
        """
        Generates a title string for the main menu based on the project's current status.
        """
        if self.p.metadata["loaded"]:
            title = (f"{self.p.mp.title}: {self.p.mp.description} | "
                    f"{self.p.mp.mc_version} | {self.p.mp.mod_loader} | "
                    f"{len(self.p.mp.mod_list)} mods | "
                    f"Version {self.p.mp.build_version} | {self.p.mp.build_date}")
            return title + '\n' + len(title)*'-'
        return "No project loaded"
