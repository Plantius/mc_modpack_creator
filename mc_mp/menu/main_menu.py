from menu import menu_func as mf, menu_options as mo
from simple_term_menu import TerminalMenu
from modpack import project as p
import standard as std
import textwrap as tw
from . import CLEAR_SCREEN

class Menu:
    def __init__(self, project: p.Project, title: str, menu_entries: list, 
                 multiselect=False, clear_screen=CLEAR_SCREEN, cursor_index=0, status: callable=None) -> None:
        """Initializes the `Menu` instance with a project."""
        self.project = project
        self.title = title
        self.menu_entries = menu_entries
        self.multi_select = multiselect
        self.clear_screen = clear_screen
        self.cursor_index = cursor_index
        self.status = status


    def display(self):
        termina
    
    def get_options(self, flags: dict) -> list:
        """Returns a list of options based on the provided flags."""
        options = []

        if flags["config"]:
            options.extend(mo.OPT_CONFIG)
        elif not flags["mod"]:
            if flags["loaded"]:
                options.extend(mo.OPT_PROJECT + mo.OPT_MODPACK + mo.OPT_MISC["config"])
            else:
                options.extend(mo.OPT_PROJECT)
        else:
            options.extend(mo.OPT_ADD_MOD)

        return options + [None] + mo.OPT_MISC["exit"]

    def get_project_status(self, entry) -> str:
        """Retrieves the status description for a given project menu entry."""
        for lst in [mo.OPT_PROJECT, mo.OPT_MODPACK, mo.OPT_ADD_MOD, mo.OPT_CONFIG]:
            i = std.get_index(mo.get_options(lst)["names"], entry)
            if i is not None:
                return mo.get_options(lst)["help"][i]

        for option in mo.OPT_MISC.keys():
            i = std.get_index(mo.get_options(mo.OPT_MISC[option])["names"], entry)
            if i is not None:
                return mo.get_options(mo.OPT_MISC[option])["help"][i]


    def get_mod_status(self, entry: str) -> str:
        """Retrieves the status of a mod based on the provided entry."""
        index = std.get_index(self.p.mp.get_mod_list_names(), entry)
        if index is not None:
            return f'{entry}: ' + tw.fill(self.p.mp.mod_list[index].description, width=100, fix_sentence_endings=True)
        return entry

    def create_config(self, title="A Menu", menu_entries=["Exit"], cursor_index=0, 
                      clear_screen=CLEAR_SCREEN, multi_select=False, show_multi_select_hint=False,
                      status_bar="No project loaded") -> dict:
        """Creates a configuration dictionary for a menu."""
        return self.mf.create_config(title, menu_entries, cursor_index, clear_screen, multi_select, show_multi_select_hint, status_bar)

    def display_menu(self, title: str, menu_entries: list, multi_select=False, status_func=None, clear_screen=CLEAR_SCREEN, cursor_index=0) -> int:
        """Displays a menu based on provided options and returns the selected index."""
        return self.mf.display_menu(title, menu_entries, multi_select, status_func, clear_screen, cursor_index)


    # Move to menu_func
    # 
    # 
    # 
    def config_menu(self, config_options: dict) -> None:
        """Displays a menu for editing project settings."""
        while True:
            selected_index = self.display_menu(
                title="Edit project settings.",
                menu_entries=mo.get_options(config_options)["names"],
                status_func=self.get_project_status
            )
            if selected_index is None:
                break

            option = mo.get_options(config_options)["ids"][selected_index]
            func = getattr(self.mf, mo.get_options(config_options)["functions"][selected_index])
            if option is mo.Option.SETTINGS and not func(self.p):
                print(f"[ERROR] Could not execute {mo.get_options(config_options)['functions'][selected_index]}")
            elif option is mo.Option.EXIT:
                break

    def rm_mod_menu(self, main_options: dict, main_index: int, func: callable) -> None:
        """Displays a menu for removing mods from the project."""
        while True:
            selected_index = self.display_menu(
                title="Select which mods to remove.",
                menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
                multi_select=True,
                status_func=self.get_mod_status
            )
            if selected_index is None:
                break

            if not func(self.p, selected_index):
                print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")

    def add_mod_menu(self, mod_options: dict) -> None:
        """Displays a menu for adding new mods to the project."""
        while True:
            selected_index = self.display_menu(
                title="Search for new mods to add to the project.",
                menu_entries=mo.get_options(mod_options)["names"],
                status_func=self.get_project_status
            )
            if selected_index is None:
                break

            option = mo.get_options(mod_options)["ids"][selected_index]
            func = getattr(self.mf, mo.get_options(mod_options)["functions"][selected_index])
            if option is mo.Option.ADD_MODS and not func(self.p):
                print(f"[ERROR] Could not execute {mo.get_options(mod_options)['functions'][selected_index]}")

            elif option is mo.Option.EXIT:
                break
    
    def update_mods_menu(self, main_options: dict, main_index: int, func: callable) -> None:
        """Displays a menu for adding new mods to the project."""
        while True:
            selected_indices = self.display_menu(
                title="Update mods in the current project.",
                menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
                multi_select=True,
                status_func=self.get_mod_status
            )
            if selected_indices is None:
                break

            if not func(self.p, selected_indices):
                print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")

    def list_mods_menu(self, main_options: dict, main_index: int, func: callable) -> None:
        """Displays a menu for adding new mods to the project."""
        cursor_index: int = 0
        while True:
            selected_index = self.display_menu(
                title="Current mods in this project.",
                menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
                status_func=self.get_mod_status,
                cursor_index=cursor_index
            )
            if selected_index is None:
                break
            cursor_index = selected_index

            if not func(self.p, selected_index):
                print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")
    # 
    # 
    # 
    # Move to menu_func

    def main_menu(self) -> None:
        """Displays the main menu and handles user interactions with different options."""
        cursor_index: int = 0
        while True:
            title = self.get_project_title()
            main_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": False})
            config_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": True, "mod": False})
            mod_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": True})

            main_index = self.display_menu(
                title=title,
                menu_entries=mo.get_options(main_options)["names"],
                status_func=self.get_project_status,
                cursor_index=cursor_index
            )
            
            if main_index is None:
                func = getattr(self.mf, mo.get_options(mo.OPT_MISC["exit"])["functions"][0])
                if not func(self.p):
                    print(f"[ERROR] Could not execute exit function")
                break

            cursor_index = main_index
            option = mo.get_options(main_options)["ids"][main_index]
            func = getattr(self.mf, mo.get_options(main_options)["functions"][main_index])

            if option is mo.Option.CONFIG:
                self.config_menu(config_options)
            elif option is mo.Option.PROJECT:
                if not func(self.p):
                    print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")
            elif option is mo.Option.ADD_MODS:
                self.add_mod_menu(mod_options) # Contains sub menu
            elif option is mo.Option.RM_MODS:
                self.rm_mod_menu(main_options, main_index, func) # Contains sub menu
            elif option is mo.Option.UPDATE_MODS:
                self.update_mods_menu(main_options, main_index, func) # Contains sub menu
            elif option is mo.Option.LIST_MODS:
                self.list_mods_menu(main_options, main_index, func) # Contains sub menu
            elif option is mo.Option.EXIT:
                if not func(self.p):
                    print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")
                break

    def get_project_title(self) -> str:
        """Generates a title string for the main menu based on the project's current status."""
        if self.p.metadata["loaded"]:
            title = (f"{self.p.mp.title}: {self.p.mp.description} | "
                    f"{self.p.mp.mc_version} | {self.p.mp.mod_loader} | "
                    f"{len(self.p.mp.mod_list)} mods | "
                    f"Version {self.p.mp.build_version} | {self.p.mp.build_date}")
            return title + '\n' + len(title)*'-'
        return "No project loaded"