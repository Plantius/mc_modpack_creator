import standard as std
from modpack_creator import Modrinth
from simple_term_menu import TerminalMenu

OPT_PROJECT = [["load_project", "Load project"], ["create_project", "Create project"], 
               ["save_project", "Save project"]]
OPT_MODPACK = [["add_mods", "Add mod(s)"], ["remove_mods", "Remove mod(s)"]]
OPT_CONFIG = [["change_project_name", "Change project name"], ["change_project_version", "Change project version"], 
              ["change_project_loader", "Change mod loader"], ["change_project_version", "Change Minecraft version"]]
OPT_EXIT = [["exit_program", "Exit program"]]

# TODO Add functionalities, make use of functions and change option layout
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

    # TODO Add generalization of common functions
    def main_menu(self) -> None:
        main_options = [i[1] for i in OPT_PROJECT] 
        if self.project.loaded:
            main_options += [i[1] for i in OPT_MODPACK]
        main_options += ["Change project settings"]
        main_options += [i[1] for i in OPT_EXIT]
        
        edit_options = [i[1] for i in OPT_CONFIG]
        edit_options += [i[1] for i in OPT_EXIT]  

            
        main_menu_exit = False
        edit_menu_exit = False
        print(main_options)
        main_menu = TerminalMenu(main_options, 
                                 title="Project Creator",
                                 clear_screen=True)
        edit_menu = TerminalMenu(edit_options, 
                                 title="Project Editor",
                                 clear_screen=True)
        while not main_menu_exit:
            main_index = main_menu.show()
            if main_index == len(main_options)-2:
                while not edit_menu_exit:
                    edit_index = edit_menu.show()

                    if edit_index >= len(edit_options)-1 or edit_index is None:
                        edit_menu_exit = True
            elif main_index >= len(main_options)-1 or main_index is None:
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
        