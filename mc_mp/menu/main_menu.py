from simple_term_menu import TerminalMenu
from modpack import project as p
import standard as std
from . import CLEAR_SCREEN, ACCEPT, OPEN, CLOSE

class Menu:
    """Class to manage terminal-based menus for interacting with modpack projects."""
    
    # Static variable to hold the main menu instance
    main_menu_instance = None
    
    def __init__(self, project: p.Project, title: str = None, menu_entries: list = None,
                 multiselect: bool = False, clear_screen: bool = CLEAR_SCREEN,
                 cursor_index: int = 0, status_bar: callable = None, actions=None,
                 parent_menu=None) -> None:
        """
        Initialize a Menu instance with the provided parameters.

        Args:
            project (p.Project): The project instance associated with this menu.
            title (str, optional): The title of the menu. Defaults to None.
            menu_entries (list, optional): A list of menu option labels. Defaults to None.
            multiselect (bool, optional): Whether multiple selections are allowed. Defaults to False.
            clear_screen (bool, optional): Whether to clear the terminal screen before showing the menu. Defaults to CLEAR_SCREEN.
            cursor_index (int, optional): The initial position of the cursor in the menu. Defaults to 0.
            status_bar (callable, optional): A callable function to display a status bar. Defaults to None.
            actions (list, optional): A list of actions corresponding to menu entries. Defaults to None.
            parent_menu (Menu, optional): The parent menu, if this menu is a submenu. Defaults to None.
        """
        self.project: p.Project = project
        self.title: str = title
        self.menu_entries: list = menu_entries or []
        self.multi_select: bool = multiselect
        self.clear_screen: bool = clear_screen
        self.cursor_index: int = cursor_index
        self.status_bar: callable = status_bar

        self.actions: list = actions or []
        self.parent_menu: Menu = parent_menu
        self.menu_active = True
        
        # Set this instance as the main menu instance if none exists
        if Menu.main_menu_instance is None:
            Menu.main_menu_instance = self

    def get_project_title(self) -> str:
        """
        Generate the title string for the main menu based on the project's current status.

        Returns:
            str: The formatted title string including project metadata.
        """
        if self.project.metadata["loaded"]:
            title = (f"{self.project.modpack.title}: {self.project.modpack.description} | "
                    f"{self.project.modpack.mc_version} | {self.project.modpack.mod_loader} | "
                    f"{len(self.project.modpack.mod_data)} mods | "
                    f"Version {self.project.modpack.build_version} | {self.project.modpack.build_date}")
            return title + '\n' + len(title) * '-'
        return "No project loaded"
    
    def update_entries(self):
        """Update the menu entries and associated actions based on the current project state."""
        self.menu_entries.clear()
        self.actions.clear()
        self.add_option("Load project", lambda: self.load_project_action())
        self.add_option("Save project", lambda: self.save_project_action())
        self.add_option("Create project", lambda: self.create_project_action())
        if self.project.metadata["loaded"]:
            self.add_option("Add mod(s)", lambda: self.add_mods_action())
        self.add_option("Exit", self.go_back)
    
    def add_option(self, option: str, action=None) -> None:
        """
        Add a new option to the menu.

        Args:
            option (str): The label of the menu option.
            action (callable, optional): The action to perform when this option is selected. Defaults to None.
        """
        self.menu_entries.append(option)
        self.actions.append(action)
    
    def display(self) -> None:
        """
        Display the menu and handle user input through TerminalMenu.
        The menu remains active until the user decides to exit.
        """
        while self.menu_active:
            self.title = self.get_project_title()
            terminal_menu = TerminalMenu(
                title=self.title,
                menu_entries=self.menu_entries,
                multi_select=self.multi_select,
                clear_screen=self.clear_screen,
                cursor_index=self.cursor_index,
                status_bar=self.status_bar
            )
            selected_index = terminal_menu.show()
            if selected_index is not None:
                self.handle_selection(selected_index)
            else:
                self.exit_submenu()

    def handle_selection(self, selected_index) -> None:
        """
        Handle the user's selection from the menu.

        Args:
            selected_index (int): The index of the selected menu option.
        """
        if selected_index < len(self.actions):
            action = self.actions[selected_index]
            if callable(action):
                if not action():
                    self.menu_active = False
                    if self.parent_menu:
                        self.parent_menu.menu_active = True
                        self.parent_menu.display()
            elif isinstance(action, Menu):
                action.display()
        else:
            std.eprint("[ERROR] Invalid menu selection.")

    def exit_submenu(self) -> None:
        """
        Handle the action to exit a submenu.
        If this menu has a parent, it will return to the parent menu; otherwise, it performs a normal exit.
        """
        if self.parent_menu:
            # Exiting a submenu
            self.menu_active = False  # Close the current menu
        else:
            # No parent menu, treat as a normal go_back
            self.go_back()
    
    def go_back(self) -> None:
        """
        Handle the action to go back to the parent menu or exit.
        If the current project is unsaved, prompt to save it before exiting.
        """
        if not self.project.metadata["saved"]:
            self.save_project_action()
        self.menu_active = False
        if self.parent_menu:
            self.parent_menu.display()
    
    def load_project_action(self) -> bool:
        """
        Handle the action to load a project from a file.
        Prompts the user to select or enter the filename of the project to load.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        if self.project.metadata["loaded"] and not self.save_project_action():
            std.eprint("[ERROR] Could not save current project.")
            return OPEN  # Keep menu open

        submenu = Menu(
            project=self.project, 
            title="Which project do you want to load?",
            menu_entries=std.get_project_files() + ["Enter filename"],
            parent_menu=self
        )
        
        def handle_selection(selected_index):
            filename = None
            if submenu.menu_entries[selected_index] == "Enter filename":
                filename = std.get_input("Please enter a project file: ")
            else:
                filename = submenu.menu_entries[selected_index]
            if filename:
                self.project.load_project(filename)
                submenu.menu_active = False
                return CLOSE  # Close sub menu (project list)
            
        submenu.handle_selection = handle_selection
        submenu.display()
        self.update_entries()  # Update menu_entries
        return OPEN  # Keep main menu open
        
    def create_project_action(self) -> bool:
        """
        Handle the action to create a new project.
        Prompts the user to enter the details required to create a new project.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        if not self.project.metadata["saved"] and not self.save_project_action():
            std.eprint("[ERROR] Could not save current project.")
            return OPEN  # Keep main menu open

        print("To create a new project, please enter the following details:")
        title = std.get_input("1. Project Title: ")
        description = std.get_input("2. Project Description: ")
        mc_version = std.get_input("3. Minecraft Version (e.g., 1.16.5): ")
        mod_loader = std.get_input("4. Mod Loader (e.g., forge, fabric): ")

        if any(not value for value in [title, description, mc_version, mod_loader]):
            return OPEN  # Keep main menu open if creation fails

        self.project.create_project(
            title=title,
            description=description,
            mc_version=mc_version,
            mod_loader=mod_loader,
        )
        self.update_entries()  # Update menu_entries
        return OPEN  # Keep main menu open
    
    def save_project_action(self) -> bool:
        """
        Handle the action to save the current project.
        Prompts the user to confirm saving and enter a filename if necessary.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        if self is Menu.main_menu_instance and not self.project.metadata["saved"]:
            if std.get_input("Do you want to save the project? y/n: ") == ACCEPT:
                filename = std.get_input("Please enter the filename to save to: ") \
                    if std.get_input("Do you want to save the project to a new file? y/n: ") == ACCEPT \
                    else self.project.metadata["filename"]
                self.project.save_project(filename)
        return OPEN  # Keep main menu open
    
    def add_mods_action(self) -> bool:
        """
        Handle the action to add mods to the current project.
        Displays a submenu to select the method of adding mods.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        submenu = Menu(
            project=self.project, 
            title="Add mod options",
            parent_menu=self
        )
        submenu.add_option("Add mod(s) by id/slug", lambda: self.add_mods_id_action())
        submenu.display()
        return OPEN  # Keep main menu open
    
    def add_mods_id_action(self) -> bool:
        """
        Handle the action to add mods by their IDs or slugs.
        Prompts the user to enter mod slugs or IDs and then selects versions to add to the project.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        names = std.get_input("Please enter mod slugs or IDs (e.g., name1 name2 ...): ")
        if not names:
            return OPEN
        
        for name in names.split():
            versions = self.project.api.list_versions(name, loaders=[self.project.modpack.mod_loader],
                                                game_versions=[self.project.modpack.mc_version])
            if not versions:
                std.eprint(f"[ERROR] No mod called {name} found.")
                continue

            submenu = Menu(
                project=self.project, 
                title=f"Which version of {name} do you want to add?",
                menu_entries=[f'{version["name"]}: Minecraft version(s): {version["game_versions"]}, {version["version_type"]}' for version in versions],
                parent_menu=self
            )
            
            def handle_selection(selected_index):
                version = versions[selected_index]
                if std.get_input(f'''{version["name"]}:
{version["changelog"]}
Do you want to add {version["name"]} to the current project? y/n ''') == ACCEPT:
                    self.project.add_mod(name, versions, selected_index)
                    submenu.menu_active = False
                    return CLOSE  # Close sub menu (version list)

            submenu.handle_selection = handle_selection
            submenu.display()
            if not submenu.menu_active:
                continue
            
        return OPEN  # Keep main menu open
        
    def search_mods_action(self):
        """Placeholder for a future feature to search for mods."""
        pass

    
    # def get_options(self, flags: dict) -> list:
    #     """Returns a list of options based on the provided flags."""
    #     options = []

    #     if flags["config"]:
    #         options.extend(mo.OPT_CONFIG)
    #     elif not flags["mod"]:
    #         if flags["loaded"]:
    #             options.extend(mo.OPT_PROJECT + mo.OPT_MODPACK + mo.OPT_MISC["config"])
    #         else:
    #             options.extend(mo.OPT_PROJECT)
    #     else:
    #         options.extend(mo.OPT_ADD_MOD)

    #     return options + [None] + mo.OPT_MISC["exit"]

    # def get_project_status(self, entry) -> str:
    #     """Retrieves the status description for a given project menu entry."""
    #     for lst in [mo.OPT_PROJECT, mo.OPT_MODPACK, mo.OPT_ADD_MOD, mo.OPT_CONFIG]:
    #         i = std.get_index(mo.get_options(lst)["names"], entry)
    #         if i is not None:
    #             return mo.get_options(lst)["help"][i]

    #     for option in mo.OPT_MISC.keys():
    #         i = std.get_index(mo.get_options(mo.OPT_MISC[option])["names"], entry)
    #         if i is not None:
    #             return mo.get_options(mo.OPT_MISC[option])["help"][i]


    # def get_mod_status(self, entry: str) -> str:
    #     """Retrieves the status of a mod based on the provided entry."""
    #     index = std.get_index(project.mp.get_mod_list_names(), entry)
    #     if index is not None:
    #         return f'{entry}: ' + tw.fill(project.mp.mod_list[index].description, width=100, fix_sentence_endings=True)
    #     return entry

    # def create_config(self, title="A Menu", menu_entries=["Exit"], cursor_index=0, 
    #                   clear_screen=CLEAR_SCREEN, multi_select=False, show_multi_select_hint=False,
    #                   status_bar="No project loaded") -> dict:
    #     """Creates a configuration dictionary for a menu."""
    #     return self.mf.create_config(title, menu_entries, cursor_index, clear_screen, multi_select, show_multi_select_hint, status_bar)

    # def display_menu(self, title: str, menu_entries: list, multi_select=False, status_func=None, clear_screen=CLEAR_SCREEN, cursor_index=0) -> int:
    #     """Displays a menu based on provided options and returns the selected index."""
    #     return self.mf.display_menu(title, menu_entries, multi_select, status_func, clear_screen, cursor_index)


    # # Move to menu_func
    # # 
    # # 
    # # 
    # def config_menu(self, config_options: dict) -> None:
    #     """Displays a menu for editing project settings."""
    #     while True:
    #         selected_index = self.display_menu(
    #             title="Edit project settings.",
    #             menu_entries=mo.get_options(config_options)["names"],
    #             status_func=self.get_project_status
    #         )
    #         if selected_index is None:
    #             break

    #         option = mo.get_options(config_options)["ids"][selected_index]
    #         func = getattr(self.mf, mo.get_options(config_options)["functions"][selected_index])
    #         if option is mo.Option.SETTINGS and not func(self.p):
    #             print(f"[ERROR] Could not execute {mo.get_options(config_options)['functions'][selected_index]}")
    #         elif option is mo.Option.EXIT:
    #             break

    # def rm_mod_menu(self, main_options: dict, main_index: int, func: callable) -> None:
    #     """Displays a menu for removing mods from the project."""
    #     while True:
    #         selected_index = self.display_menu(
    #             title="Select which mods to remove.",
    #             menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
    #             multi_select=True,
    #             status_func=self.get_mod_status
    #         )
    #         if selected_index is None:
    #             break

    #         if not func(self.p, selected_index):
    #             print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")

    # def add_mod_menu(self, mod_options: dict) -> None:
    #     """Displays a menu for adding new mods to the project."""
    #     while True:
    #         selected_index = self.display_menu(
    #             title="Search for new mods to add to the project.",
    #             menu_entries=mo.get_options(mod_options)["names"],
    #             status_func=self.get_project_status
    #         )
    #         if selected_index is None:
    #             break

    #         option = mo.get_options(mod_options)["ids"][selected_index]
    #         func = getattr(self.mf, mo.get_options(mod_options)["functions"][selected_index])
    #         if option is mo.Option.ADD_MODS and not func(self.p):
    #             print(f"[ERROR] Could not execute {mo.get_options(mod_options)['functions'][selected_index]}")

    #         elif option is mo.Option.EXIT:
    #             break
    
    # def update_mods_menu(self, main_options: dict, main_index: int, func: callable) -> None:
    #     """Displays a menu for adding new mods to the project."""
    #     while True:
    #         selected_indices = self.display_menu(
    #             title="Update mods in the current project.",
    #             menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
    #             multi_select=True,
    #             status_func=self.get_mod_status
    #         )
    #         if selected_indices is None:
    #             break

    #         if not func(self.p, selected_indices):
    #             print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")

    # def list_mods_menu(self, main_options: dict, main_index: int, func: callable) -> None:
    #     """Displays a menu for adding new mods to the project."""
    #     cursor_index: int = 0
    #     while True:
    #         selected_index = self.display_menu(
    #             title="Current mods in this project.",
    #             menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
    #             status_func=self.get_mod_status,
    #             cursor_index=cursor_index
    #         )
    #         if selected_index is None:
    #             break
    #         cursor_index = selected_index

    #         if not func(self.p, selected_index):
    #             print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")
    # # 
    # # 
    # # 
    # # Move to menu_func

    #     """Displays the main menu and handles user interactions with different options."""
        # cursor_index: int = 0
        # while True:
        #     title = self.get_project_title()
        #     main_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": False})
        #     config_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": True, "mod": False})
        #     mod_options = self.get_options({"loaded": self.p.metadata["loaded"], "config": False, "mod": True})

        #     main_index = self.display_menu(
        #         title=title,
        #         menu_entries=mo.get_options(main_options)["names"],
        #         status_func=self.get_project_status,
        #         cursor_index=cursor_index
        #     )
            
        #     if main_index is None:
        #         func = getattr(self.mf, mo.get_options(mo.OPT_MISC["exit"])["functions"][0])
        #         if not func(self.p):
        #             print(f"[ERROR] Could not execute exit function")
        #         break

        #     cursor_index = main_index
        #     option = mo.get_options(main_options)["ids"][main_index]
        #     func = getattr(self.mf, mo.get_options(main_options)["functions"][main_index])

        #     if option is mo.Option.CONFIG:
        #         self.config_menu(config_options)
        #     elif option is mo.Option.PROJECT:
        #         if not func(self.p):
        #             print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")
        #     elif option is mo.Option.ADD_MODS:
        #         self.add_mod_menu(mod_options) # Contains sub menu
        #     elif option is mo.Option.RM_MODS:
        #         self.rm_mod_menu(main_options, main_index, func) # Contains sub menu
        #     elif option is mo.Option.UPDATE_MODS:
        #         self.update_mods_menu(main_options, main_index, func) # Contains sub menu
        #     elif option is mo.Option.LIST_MODS:
        #         self.list_mods_menu(main_options, main_index, func) # Contains sub menu
        #     elif option is mo.Option.EXIT:
        #         if not func(self.p):
        #             print(f"[ERROR] Could not execute {mo.get_options(main_options)['functions'][main_index]}")
        #         break

    