import standard as std
from modpack_creator import Modrinth

OPT_PROJECT = [["load_project", "Load project"], ["create_project", "Create project"], 
               ["save_project", "Save project"]]
OPT_MODPACK = [["add_mods", "Add mod(s)"], ["remove_mods", "Remove mod(s)"]]
OPT_CONFIG = [["change_project_name", "Change project name"], ["change_project_version", "Change project version"], 
              ["change_project_loader", "Change mod loader"], ["change_project_version", "Change Minecraft version"]]


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
        done = False
        opt = [f for f in std.get_functions(self) if not f.startswith('main')]
        print(opt)

        print("Modpack Creator.\n------------------------------------------------")
        print("Please select an option from the following list:")
        while not done:
            self.main_menu_options()
            inp = input("Please enter your selected option: ")
            if not inp.isnumeric():
                print("Selection contains non-numbers.")
                continue
            inp = int(inp)
            if inp <= 0 or inp > len(opt):
                print(f"Option {inp} is not a valid option.")
                return
            print(getattr(self, opt[inp-1]))
        
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
        