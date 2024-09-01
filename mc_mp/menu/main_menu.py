"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/menu/main_menu.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from simple_term_menu import TerminalMenu
from modpack import project as p
import standard as std
import asyncio
from . import CLEAR_SCREEN, ACCEPT, OPEN

class Menu:
    # Static variable to hold the main menu instance
    main_menu_instance = None
    
    def __init__(self, project: p.Project, title: str="", menu_entries=None,
                 multi_select: bool = False, clear_screen: bool = CLEAR_SCREEN,
                 cursor_index: int = 0, status_bar: callable = None, actions=None,
                 parent_menu=None, help: list[str]=None) -> None:
        """
        Initialize the menu with project details and menu options.
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
        Get the title and details of the current project.
        """
        if self.project.metadata["loaded"]:
            return (f"{self.project.modpack.title}: {self.project.modpack.description} | "
                    f"{self.project.modpack.mc_version} | {self.project.modpack.mod_loader} | "
                    f"{len(self.project.modpack.mod_data)} mods | "
                    f"Version {self.project.modpack.build_version}")
        return "No project loaded"
    
    def get_entry_help(self, entry) -> str:
        """
        Get help text for a specific menu entry.
        """
        index = std.get_index(self.menu_entries, entry)
        if index is None:
            std.eprint("Could not find entry.")
            return entry
        return self.help[index]
    
    def get_main_menu_entries(self) -> None:
        """
        Populate the main menu with available options.
        """
        self.menu_entries.clear()
        self.actions.clear()
        self.help.clear()

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
        """
        Get description of a specific mod entry.
        """
        index = std.get_index(self.project.modpack.get_mods_name_ver(), entry)
        if index < 0:
            std.eprint("Could not find entry.")
            return entry
        return self.project.modpack.get_mods_descriptions()[index]
    
    def add_option(self, option: str, action=None, help: str="") -> None:
        """
        Add an option to the menu with a corresponding action and help text.
        """
        self.menu_entries.append(option)
        self.actions.append(action)
        self.help.append(help)
    
    async def display(self) -> None:
        """
        Display the menu and handle user selections asynchronously.
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
        Handle the user's menu selection and invoke the corresponding action.
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
        Exit the current menu and return to the parent menu if available.
        """
        if self.parent_menu:
            self.menu_active = False  # Close the current menu
        else:
            await self.close_self()
    
    async def close_self(self) -> None:
        """
        Save the project if necessary and close the menu.
        """
        if not self.project.metadata["saved"]:
            await self.save_project_action()
        self.menu_active = False
    
    async def load_project_action(self) -> bool:
        """
        Handle loading a project and prompt for a filename or select from existing files.
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
        Handle creating a new project by prompting for details.
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
        Handle saving the current project to a specified filename.
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
        Display the submenu for adding mods by ID or searching for mods.
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
        Add mods to the project based on provided IDs and handle dependencies.
        """
        ids = [id for id in ids if not self.project.is_mod_installed(id)]
        info = await self.project.fetch_mods_by_ids(ids)

        if not any(info["project_info"]) or not any(info["versions"]):
            std.eprint(f"[ERROR] Could not retrieve mods.")
            return OPEN
        
        for versions, project_info in zip(info["versions"], info["project_info"]):
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
        """
        Prompt for mod IDs or slugs and initiate adding mods.
        """
        names = std.get_input("Please enter mod slugs or IDs (e.g., name1 name2 ...): ")
        if not names:
            return OPEN
        return self.add_mods_action(names.split())
        
    
    # TODO Unify search mods and add mods
    async def search_mods_action(self):
        """
        Search for mods based on a query and selected facets.
        """
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
            selected_mod_ids = [results["hits"][i]["project_id"] for i in selected_index if not self.project.is_mod_installed(results["hits"][i]["project_id"])]
            if len(selected_index) == 1:
                selected_mod = results["hits"][selected_index[0]]
                if input(f'''{selected_mod["title"]} \nClient side: {selected_mod["client_side"]}\nServer side: {selected_mod["server_side"]}\n\n{selected_mod["description"]}\nLink to mod https://modrinth.com/mod/{selected_mod["slug"]}\n\tDo you want to add this mod to the current project? y/n ''') != ACCEPT:
                    return

            await self.add_mods_action(selected_mod_ids)

        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN
    
    async def update_mods_action(self) -> bool:
        """
        Display submenu for updating mods in the current project.
        """
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
            ids = [[id.project_id for id in self.project.modpack.mod_data][i] for i in selected_index]
            info = await self.project.fetch_mods_by_ids(ids)
            if not any(info["project_info"]) or not any(info["versions"]):
                std.eprint(f"[ERROR] Could not retrieve mods.")
                return
            
            for index, latest_version, project_info in zip(selected_index, info["versions"], info["project_info"]):
                if self.project.is_date_newer(latest_version[0]["date_published"], self.project.modpack.mod_data[index].date_published):
                    inp = std.get_input(f"There is a newer version available for {self.project.modpack.mod_data[index].name}, do you want to upgrade? y/n {self.project.modpack.mod_data[index].version_number} -> {latest_version[0]['version_number']} ")
                    if inp == ACCEPT:
                        await self.project.update_mod(latest_version, project_info, index)
                print(f"{self.project.modpack.get_mods_name_ver()[index]} is up to date")

        
        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN
    
    async def remove_mods_action(self) -> bool:
        """
        Display submenu for removing mods from the current project.
        """
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
                await self.project.rm_mod(i) 

        submenu.handle_selection = handle_selection
        await submenu.display()
        return OPEN
    
    
    async def change_settings_menu(self) -> None:
        """
        Display submenu for changing project settings.
        """
        submenu = Menu(
            project=self.project,
            title="Change project settings",
            menu_entries=["Change title", "Change description", "Change Minecraft version", "Change mod loader", "Change build version"],
            parent_menu=self
        )
        
        async def handle_selection(selected_index):
            if selected_index == 0:
                new_title = std.get_input("Enter new project title: ")
                self.project.modpack.title = new_title
            elif selected_index == 1:
                new_description = std.get_input("Enter new project description: ")
                self.project.modpack.description = new_description
            elif selected_index == 2:
                new_mc_version = std.get_input("Enter new Minecraft version: ")
                self.project.modpack.mc_version = new_mc_version
            elif selected_index == 3:
                new_mod_loader = std.get_input("Enter new mod loader: ")
                self.project.modpack.mod_loader = new_mod_loader
            elif selected_index == 4:
                new_build_version = std.get_input("Enter new build version: ")
                self.project.modpack.build_version = new_build_version

        
        submenu.handle_selection = handle_selection
        await submenu.display()
    
    async def list_mods_action(self) -> bool:
        """
        Display submenu for listing mods in the current project.
        """
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
