import standard as std
from modpack_creator import Modrinth
from simple_term_menu import TerminalMenu

OPT_PROJECT = [["load_project", "Load project"], ["create_project", "Create project"], 
               ["save_project", "Save project"]]
OPT_MODPACK = [["add_mods", "Add mod(s)"], ["remove_mods", "Remove mod(s)"]]
OPT_CONFIG = [["change_project_name", "Change project name"], ["change_project_version", "Change project version"], 
              ["change_project_loader", "Change mod loader"], ["change_project_version", "Change Minecraft version"]]
OPT_EXIT = [["exit_program", "Exit program"]]

class menu:
    project: Modrinth.project

    def __init__(self, project: Modrinth.project) -> None:
        self.project = project
    
    def main_menu_options(self) -> None:
        count = 1
        if not self.project.loaded:
            print("--- No project is loaded. ---")
        for i in OPT_PROJECT:
            print(f"{count}: {i[1]}")
            count += 1
        if self.project.loaded:
            for i in OPT_MODPACK:
                print(f"{count}: {i[1]}")
                count += 1
            

        print(f"{count}: Exit program")

    def main_menu(self) -> None:
        options = [i[1] for i in OPT_PROJECT]
        if self.project.loaded:
            options += [i[1] for i in OPT_MODPACK]
        options += "Change project settings"
        options += [i[1] for i in OPT_EXIT]
        main_menu_exit = False
        print(options)
        main_menu = TerminalMenu(options, 
                                 title="Modpack Creator",
                                 clear_screen=True)
        edit_menu = TerminalMenu(options, 
                                 title="Modpack Creator",
                                 clear_screen=True)
        while not main_menu_exit:
            main_index = main_menu.show()
            if main_index == len(options)-2:
                edit_index = ed
            elif:
                main_index >= len(options)-1 or main_index is None:
                main_menu_exit = True
        
    def load_project(self) -> bool:
        """Loads a project"""
        print("Please enter a project filename: ")
        filename = str(input())
        if not filename.isalnum():
            print("Filename contains non-ASCII characters.")
            return False
        
        return True
    
    def exit_program(self) -> None:
        """Exits the program"""
        print("Exiting program.")
        if not self.project.saved:
            input = bool(input("Do you want to save the project?"))
            if input:
                self.project.save_project(self.project.filename)
                print("Project saved.")
            exit(0)
        