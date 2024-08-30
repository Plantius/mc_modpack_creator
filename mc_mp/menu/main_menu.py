from simple_term_menu import TerminalMenu
from modpack import project as p
import standard as std
import asyncio
from . import CLEAR_SCREEN, ACCEPT, OPEN

class Menu:
    """Class to manage terminal-based menus for interacting with modpack projects."""
    
    # Static variable to hold the main menu instance
    main_menu_instance = None
    
    def __init__(self, project: p.Project, title: str="", menu_entries=None,
                 multi_select: bool = False, clear_screen: bool = CLEAR_SCREEN,
                 cursor_index: int = 0, status_bar: callable = None, actions=None,
                 parent_menu=None, help: list[str]=None) -> None:
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
        self.menu_entries = menu_entries or []
        self.multi_select: bool = multi_select
        self.clear_screen: bool = clear_screen
        self.cursor_index: int = cursor_index
        self.status_bar: callable = status_bar

        self.actions: list = actions or []
        self.help: list = help or []
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
            return (f"{self.project.modpack.title}: {self.project.modpack.description} | "
                    f"{self.project.modpack.mc_version} | {self.project.modpack.mod_loader} | "
                    f"{len(self.project.modpack.mod_data)} mods | "
                    f"Version {self.project.modpack.build_version}")
        return "No project loaded"
    
    def get_entry_help(self, entry) -> str:
        """Retrieves the status description for a given project menu entry."""
        index = std.get_index(self.menu_entries, entry)
        if index is None:
            std.eprint("Could not find entry.")
            return entry
        return self.help[index]
    
    def get_main_menu_entries(self) -> None:
        """Initialize the main menu entries and associated actions."""
        self.menu_entries.clear(); self.actions.clear(); self.help.clear()

        self.add_option("Load project", self.load_project_action, "Load a project file")
        self.add_option("Save project", self.save_project_action, "Save the current project")
        self.add_option("Create project", self.create_project_action, "Create a new project")
        if self.project.metadata["loaded"]:
            self.add_option("Add mod(s)", self.add_mods_menu, "Add new mods to the current project")
            self.add_option("List current mods", self.list_mods_action, "List all mods in the current project")
            self.add_option("Remove mod(s)", self.remove_mods_action, "Remove mods from the current project")
            self.add_option("Update mod(s)", self.update_mods_action, "Update mods in the current project")
            self.add_option("Change project settings", self.change_settings_menu, "Change the project's title, description, etc.")
        
        self.add_option("Exit", self.close_self, "Exit the current menu")
    
    def get_entry_description(self, entry) -> str:
        """Retrieves the description for a given mod entry."""
        index = std.get_index(self.project.modpack.get_mods_name_ver(), entry)
        if index < 0:
            std.eprint("Could not find entry.")
            return entry
        return self.project.modpack.get_mods_descriptions()[index]
    
    
    def add_option(self, option: str, action=None, help: str="") -> None:
        """
        Add a new option to the menu.

        Args:
            option (str): The label of the menu option.
            action (callable, optional): The action to perform when this option is selected. Defaults to None.
        """
        self.menu_entries.append(option)
        self.actions.append(action)
        self.help.append(help)
    
    async def display(self) -> None:
        """
        Display the menu and handle user input through TerminalMenu.
        The menu remains active until the user decides to exit.
        """
        while self.menu_active:
            if self is Menu.main_menu_instance:
                self.title = self.get_project_title
                self.get_main_menu_entries()
            terminal_menu = TerminalMenu(
                title=self.title() if callable(self.title) else self.title,
                menu_entries=self.menu_entries() if callable(self.menu_entries) else self.menu_entries,
                multi_select=self.multi_select,
                clear_screen=self.clear_screen,
                cursor_index=self.cursor_index,
                status_bar=self.status_bar
            )
            selected_index = terminal_menu.show()
            if selected_index is not None:
                await self.handle_selection(selected_index)
            else:
                await self.exit_menu()

    async def handle_selection(self, selected_index) -> None:
        """
        Handle the user's selection from the menu.

        Args:
            selected_index (int): The index of the selected menu option.
        """
        if selected_index < len(self.actions):
            action = self.actions[selected_index]
            if asyncio.iscoroutinefunction(action):
                await action()
            elif callable(action):
                action_result = action()
                if asyncio.iscoroutine(action_result):
                    await action_result
            elif isinstance(action, Menu):
                await action.display()
            if not self.menu_active and self.parent_menu:
                self.parent_menu.menu_active = True
                await self.parent_menu.display()
        else:
            std.eprint("[ERROR] Invalid menu selection.")

    async def exit_menu(self) -> None:
        """
        Handle the action to exit a submenu.
        If this menu has a parent, it will return to the parent menu; otherwise, it performs a normal exit.
        """
        if self.parent_menu:
            self.menu_active = False  # Close the current menu
        else:
            await self.close_self()
    
    async def close_self(self) -> None:
        """
        Handle the action to go back to the parent menu or exit.
        If the current project is unsaved, prompt to save it before exiting.
        """
        if not self.project.metadata["saved"]:
            await self.save_project_action()
        self.menu_active = False
    
    async def load_project_action(self) -> bool:
        """
        Handle the action to load a project from a file.
        Prompts the user to select or enter the filename of the project to load.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        if self.project.metadata["loaded"] and not await self.save_project_action():
            std.eprint("[ERROR] Could not save current project.")
            return OPEN  # Keep menu open

        submenu = Menu(
            project=self.project, 
            title="Which project do you want to load?",
            menu_entries=std.get_project_files() + ["Enter filename"],
            parent_menu=self
        )
        
        async def handle_selection(selected_index):
            filename = None
            if submenu.menu_entries[selected_index] == "Enter filename":
                filename = std.get_input("Please enter a project file: ")
            else:
                filename = submenu.menu_entries[selected_index]
            if filename:
                self.project.load_project(filename)
                submenu.menu_active = False
            
        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN  # Keep main menu open
        
    async def create_project_action(self) -> bool:
        """
        Handle the action to create a new project.
        Prompts the user to enter the details required to create a new project.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        if not self.project.metadata["saved"] and not await self.save_project_action():
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
        return OPEN  # Keep main menu open
    
    async def save_project_action(self) -> bool:
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
    
    async def add_mods_menu(self) -> bool:
        """
        Handle the action to add mods to the current project.
        Displays a submenu to select the method of adding mods.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        submenu = Menu(
            project=self.project, 
            title=self.get_project_title,
            parent_menu=self
        )
        submenu.add_option("Add mods by id/slug", self.add_mods_id_action)
        submenu.add_option("Search for mods", self.search_mods_action)
        await submenu.display()
        return OPEN  # Keep main menu open
    
    async def add_mods_action(self, ids: list[str]) -> bool:
        """
        Handle the action to add mods by their IDs or slugs.
        Prompts the user to enter mod slugs or IDs and then selects versions to add to the project.

        Returns:
            bool: Status indicating whether to keep the main menu open (OPEN) or close it (CLOSE).
        """
        mods_versions_info_all = await self.project.fetch_mods_by_ids(ids)

        if not any(mods_versions_info_all):
            std.eprint(f"[ERROR] Could not retrieve mods.")
            return OPEN
        
        for versions, project_info in [(p["versions"], p["project_info"]) for p in mods_versions_info_all]:
            submenu = Menu(
                project=self.project, 
                title=f"Which version of {project_info['title']} do you want to add?",
                menu_entries=[f'''{project_info["title"]} - {version["version_number"]}: Minecraft version(s): {version["game_versions"]}, {version["version_type"]}''' for version in versions],
                parent_menu=self)
            
            async def handle_selection(selected_index):
                version = versions[selected_index]
                if std.get_input(f'''{version["name"]}: \n{version["changelog"]}\n\tDo you want to add {version["name"]} to the current project? y/n ''') == ACCEPT:
                    await self.project.add_mod(project_info["slug"], version, 
                                         project_info=project_info)
                    
                    if len(version["dependencies"]) > 0:
                        required_ids = [dep["project_id"] for dep in version["dependencies"] if dep["dependency_type"] == "required" and not self.project.is_mod_installed(dep["project_id"])]
                        if required_ids:
                            await self.add_mods_action(required_ids)
                    submenu.menu_active = False  # Close sub menu (version list)

            submenu.handle_selection = handle_selection
            await submenu.display()
        return OPEN  # Keep main menu open
    
    def add_mods_id_action(self) -> bool:
        names = std.get_input("Please enter mod slugs or IDs (e.g., name1 name2 ...): ")
        if not names:
            return OPEN
        return self.add_mods_action(names.split())
        
    
    # TODO Unify search mods and add mods
    async def search_mods_action(self):
        """Placeholder for a future feature to search for mods."""
        query = std.get_input("Please enter a term to search for: ")

        kwargs = {
            "query": query,
            "facets": [
                [f"categories:{self.project.modpack.mod_loader}"],
                [f"versions:{self.project.modpack.mc_version}"]
            ],
            "limit": 200
        }

        if std.get_input("Do you want to enter additional facets? y/n: ") == ACCEPT:
            facets = std.get_input("Enter the facets you want to search with (e.g., modloader(s), minecraft version(s)): ")
            if facets is None:
                std.eprint("[ERROR] No facets given.")
                return False
            temp = [[f"{key}:{item}" for item in value.split()] for key, value in zip(["categories", "versions"], facets.split(','))]
            kwargs["facets"] = [[item] for facet in temp for item in facet] + [["project_type:mod"]]
        results = await self.project.search_mods(**kwargs)

        if not results:
            return OPEN
        submenu = Menu(
                project=self.project, 
                title="Which entries do you want to add? Select one option to see its details.",
                menu_entries=[f'{mod["title"]}: ' for mod in results["hits"]],
                multi_select=True
            )
          
        async def handle_selection(selected_index):
            selected_mod_ids = [results["hits"][i]["project_id"] for i in selected_index]
            if len(selected_index) == 1:
                selected_mod = results["hits"][selected_index[0]]
                if input(f'''{selected_mod["title"]} \nClient side: {selected_mod["client_side"]}\nServer side: {selected_mod["server_side"]}\n\n{selected_mod["description"]}\nLink to mod https://modrinth.com/mod/{selected_mod["slug"]}\n\tDo you want to add this mod to the current project? y/n ''') != ACCEPT:
                    return

            await self.add_mods_action(selected_mod_ids)

        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN
    
    async def update_mods_action(self) -> bool:
        """View all mods in the current project."""
        if len(self.project.modpack.mod_data) == 0:
            return OPEN  # Keep main menu open
        
        submenu = Menu(
                project=self.project, 
                title="Update mods in the current project:",
                menu_entries=self.project.modpack.get_mods_name_ver,  # Updatable
                status_bar=self.get_entry_description,
                multi_select=True
            )
          
        async def handle_selection(selected_index):
            if len(self.project.modpack.mod_data) == 0:
                return
            
            await self.project.update_mod(selected_index)
            
        
        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN
    
    async def remove_mods_action(self) -> bool:
        """View all mods in the current project."""
        if len(self.project.modpack.mod_data) == 0:
            return OPEN  # Keep main menu open
        
        submenu = Menu(
                project=self.project, 
                title="Select which mods to remove:",
                menu_entries=self.project.modpack.get_mods_name_ver,  # Updatable
                status_bar=self.get_entry_description,
                multi_select=True
            )
        async def handle_selection(selected_index):
            if len(self.project.modpack.mod_data) == 0:
                return
            for i in sorted(selected_index, reverse=True):
                self.project.rm_mod(i) 

        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN
    
    
    async def change_settings_menu(self) -> bool:
        submenu = Menu(
            project=self.project, 
            title=self.get_project_title,
            parent_menu=self
        )
        submenu.add_option("Change Title", self.change_title_action, "Change the modpack title")
        submenu.add_option("Change Description", self.change_description_action, "Change the modpack's description")
        submenu.add_option("Change Minecraft Version", self.change_mc_version_action, "Change the modpack's minecraft version")
        submenu.add_option("Change Modloader", self.change_modloader_action, "Change the modpack's modloader")
        submenu.add_option("Change Build Version", self.change_build_action, "Change the modpack's build version")
        await submenu.display()
        return OPEN
    
    def change_project_attribute(self, attribute: str, prompt: str) -> bool:
        """Change a project attribute based on user input."""
        new_value = std.get_input(prompt)
        if not new_value:
            return OPEN

        setattr(self.project.modpack, attribute, new_value)
        self.project.metadata["saved"] = False
        return OPEN
    
    async def change_title_action(self) -> bool:
        return self.change_project_attribute("title", "Please enter a new title: ")

    async def change_description_action(self) -> bool:
        return self.change_project_attribute("description", "Please enter the new description: ")

    async def change_modloader_action(self) -> bool:
        return self.change_project_attribute("mod_loader", "Please enter a new modloader: ")

    async def change_mc_version_action(self) -> bool:
        return self.change_project_attribute("mc_version", "Please enter a new Minecraft version: ")
    
    async def change_build_action(self) -> bool:
        return self.change_project_attribute("build_version", "Please enter the new version: ")

    
    async def list_mods_action(self) -> bool:
        """View all mods in the current project."""
        if len(self.project.modpack.mod_data) == 0:
            return OPEN  # Keep main menu open
        
        submenu = Menu(
                project=self.project, 
                title=f"The mods currently in this project.",
                menu_entries=self.project.modpack.get_mods_name_ver,  # Updatable
                status_bar=self.get_entry_description
            )
          
        async def handle_selection(selected_index):
            std.get_input(f"Changelog of {self.project.modpack.mod_data[selected_index].name}: {self.project.modpack.mod_data[selected_index].changelog}")

        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN