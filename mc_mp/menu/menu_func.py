import modpack.project as p
import standard as std
from simple_term_menu import TerminalMenu
from menu import ACCEPT, CLEAR_SCREEN

class MenuFunctions():
    def __init__(self) -> None:
        pass
    
    def create_config(self, title="A Menu", menu_entries=["Exit"], cursor_index=0, 
                      clear_screen=CLEAR_SCREEN, multi_select=False, show_multi_select_hint=False,
                      status_bar="No project loaded") -> dict:
        """Creates a configuration dictionary for a menu."""
        return {
            "title": title,
            "menu_entries": menu_entries,
            "cursor_index": cursor_index,
            "clear_screen": clear_screen,
            "multi_select": multi_select,
            "show_multi_select_hint": show_multi_select_hint,
            "status_bar": status_bar
        }

    def display_menu(self, title: str, menu_entries: dict, multi_select=False, status_func=None, clear_screen=CLEAR_SCREEN) -> int:
        """Displays a menu based on provided options and returns the selected index."""
        menu_config = self.create_config(
            title=title,
            menu_entries=menu_entries,
            multi_select=multi_select,
            status_bar=status_func,
            clear_screen=clear_screen
        )
        menu = TerminalMenu(**menu_config)
        return menu.show()
    

    def load_project(self, project: p.Project) -> bool:
        """Load a project from a specified file, saving the current project if needed."""
        if project.metadata["loaded"] and not self.save_project(project):
            std.eprint("[ERROR] Could not save current project.")
            return False
        
        # Display menu
        menu_entries = std.get_project_files() + [None, "Enter filename"]
        selected_index = self.display_menu(
            title="Which project do you want to load?",
            menu_entries=menu_entries
        )
        if selected_index is None:
            return True

        if menu_entries[selected_index] == "Enter filename":
            filename = std.get_input("Please enter a project file: ")
            if filename is None:
                return False
        else:
            filename = menu_entries[selected_index]
        project.load_project(filename)
        return True

    def create_project(self, project: p.Project) -> bool:
        """Create a new project with user-defined details and save it."""
        if project.metadata["loaded"] and not self.save_project(project):
            std.eprint("[ERROR] Could not save current project.")
            return False

        title = std.get_input("Please enter a project name: ")
        description = std.get_input("Please enter a description: ")
        mc_version = std.get_input("Please enter the project's Minecraft version: ")
        mod_loader = std.get_input("Please enter the project's modloader: ")

        if any(value is None for value in [title, description, mc_version, mod_loader]):
            return False

        project.create_project(
            title=title,
            description=description,
            mc_version=mc_version,
            mod_loader=mod_loader,
        )
        return True

    def save_project(self, project: p.Project) -> bool:
        """Save the current project to a file, optionally with a new filename."""
        if not project.metadata["saved"]:
            if std.get_input("Do you want to save the project? y/n: ") == ACCEPT:
                if std.get_input("Do you want to save the project to a new file? y/n: ") == ACCEPT:
                    filename = std.get_input("Please enter the filename to save to: ")
                    if filename is None:
                        return False
                    project.save_project(filename)
                else:
                    project.save_project(project.metadata["filename"])
                project.metadata["saved"] = True
        return True

    # TODO Add more info when multiple mods are selected
    def search_mods(self, project: p.Project) -> bool:
        """Search for mods based on user input and add selected mods to the project."""
        query = std.get_input("Please enter a term to search for: ")

        kwargs = {
            "query": query,
            "facets": [
                [f"categories:{project.mp.mod_loader}"],
                [f"versions:{project.mp.mc_version}"]
            ],
            "limit": 200
        }

        if std.get_input("Do you want to enter additional facets? y/n: ") == ACCEPT:
            facets = std.get_input("Enter the facets you want to search with (e.g., modloader(s), minecraft version(s)): ")
            if facets is None:
                std.eprint("[ERROR] No facets given.")
                return False
            temp = [[f"{key}:{item}" for item in value.split()] for key, value in zip(["categories", "versions"], facets.split(','))]
            kwargs["facets"] = [item for facet in temp for item in facet] + ["project_type:mod"]

        results = project.search_project(**kwargs)

        while True:
            selected_indices = self.display_menu(
                title="Which entries do you want to add? Select one option to see its details.",
                menu_entries=[f'{mod["title"]}: ' for mod in results["hits"]],
                multi_select=True
            )
            if selected_indices is None:
                return True
            
            if len(selected_indices) == 1:
                selected_mod = results["hits"][selected_indices[0]]
                if input(f'''{selected_mod["title"]}
    Client side: {selected_mod["client_side"]}
    Server side: {selected_mod["server_side"]}

{selected_mod["description"]}
Link to mod https://modrinth.com/mod/{selected_mod["slug"]}
    Do you want to add this mod to the current project? y/n ''') != ACCEPT:
                    continue
            for i in selected_indices:
                res = self.add_mods(project, results["hits"][i]["slug"])
            return res


    def add_mods_input(self, project: p.Project) -> bool:
        """Add multiple mods to the current project based on user input."""
        names = std.get_input("Please enter mod slugs or IDs (e.g., name1 name2 ...): ")
        if not names:
            return False
        
        return all(self.add_mods(project, name) for name in names.split())


    # TODO: Ask for user confirmation when selecting mod to add 
    def add_mods(self, project: p.Project, name: str) -> bool:
        """Add a mod to the current project by its name."""
        if not project.is_slug_valid(name):
            std.eprint("[ERROR] Invalid mod name/id.")
            return False

        versions = project.list_versions(name, loaders=[project.mp.mod_loader], game_versions=[project.mp.mc_version])
        if versions is None:
            std.eprint(f"[ERROR] No mod called {name} found.")
            return False
        while True:
            selected_index = self.display_menu(
                title=f"Which version of {name} do you want to add?",
                menu_entries=[f'{version["name"]}: minecraft version(s): {version["game_versions"]}, {version["version_type"]}' for version in versions],
            )
            if selected_index is None:
                return True

            if input(f'{versions[selected_index]["name"]}:\n{versions[selected_index]["changelog"]}\nDo you want to add this mod to the current project? y/n ') is ACCEPT:
                return project.add_mod(name, versions, selected_index)


    def remove_mods(self, project: p.Project, indices) -> bool:
        """Remove mods from the current project based on their indices."""
        if indices is None or len(project.mp.mod_list) == 0:
            return False

        for i in sorted(indices, reverse=True):
            res = project.rm_mod(i)
        
        project.metadata["saved"] = False
        return res
    def update_mods(self, project: p.Project) -> bool:
        """Update all mods in the current project."""
        while True:
            selected_indices = self.display_menu(
                title="Update mods in the current project.",
                menu_entries=self.p.mp.get_mod_list_names() or ["No mods in project"],
                multi_select=True,
                status_func=self.get_mod_status
            )
            if selected_indices is None or len(project.mp.mod_list) == 0:
                break

            res = project.update_mod(selected_indices)
            project.metadata["saved"] = False
            return res

    def change_project_attribute(self, project: p.Project, attribute: str, prompt: str) -> bool:
        """Change a project attribute based on user input."""
        new_value = std.get_input(prompt)
        if not new_value:
            return False

        setattr(project.mp, attribute, new_value)
        project.metadata["saved"] = False
        return True

    def change_project_title(self, project: p.Project) -> bool:
        """Change the name of the current project."""
        return self.change_project_attribute(project, "title", "Please enter a new name: ")

    def change_project_description(self, project: p.Project) -> bool:
        """Change the description of the current project."""
        return self.change_project_attribute(project, "description", "Please enter a new description: ")

    def change_project_version(self, project: p.Project) -> bool:
        """Change the version of the current project."""
        return self.change_project_attribute(project, "build_version", "Please enter a new version: ")

    def change_project_loader(self, project: p.Project) -> bool:
        """Change the modloader of the current project."""
        return self.change_project_attribute(project, "mod_loader", "Please enter a new modloader: ")

    def change_mc_version(self, project: p.Project) -> bool:
        """Change the Minecraft version of the current project."""
        return self.change_project_attribute(project, "mc_version", "Please enter a new Minecraft version: ")

    def exit_program(self, project: p.Project) -> bool:
        """Exit the program, prompting to save the project if necessary."""
        return self.save_project(project) if not project.metadata["saved"] else True

    def placeholder(self) -> bool:
        """Placeholder function that always returns `True`."""
        return True
