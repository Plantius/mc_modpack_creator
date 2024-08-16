import standard as std
from modpack_creator import Modrinth
from .options import PROJECT_OPTIONS, MOD_OPTIONS, CONFIG_OPTIONS, EXIT_OPTIONS


class menu:
    project: Modrinth.project

    def __init__(self, project: Modrinth.project) -> None:
        self.project = project
    
    def main_menu_options(self) -> None:
        count = 1
        if not self.project.loaded:
            print("--- No project is loaded. ---")
        for i in PROJECT_OPTIONS:
            print(f"{count}: {list(i.values())[0]}")
            count += 1
        if self.project.loaded:
            for i in MOD_OPTIONS:
                print(f"{count}: {list(i.values())[0]}")
                count += 1
        for i in EXIT_OPTIONS:
            print(f"{count}: {list(i.values())[0]}")
            count += 1

    def main_menu(self) -> None:
        done = False
        opt = [func for func in std.get_functions(self) if not func.startswith('main')]
        print(opt)

        mapped_options = {(1, len(PROJECT_OPTIONS)): PROJECT_OPTIONS, 
                          (len(PROJECT_OPTIONS)+1, len(PROJECT_OPTIONS)+len(MOD_OPTIONS)): MOD_OPTIONS,
                          (len(PROJECT_OPTIONS)+len(MOD_OPTIONS)+1, len(PROJECT_OPTIONS)+len(MOD_OPTIONS)+len(CONFIG_OPTIONS)): CONFIG_OPTIONS,
                          (len(PROJECT_OPTIONS)+len(MOD_OPTIONS)+len(CONFIG_OPTIONS)+1, len(PROJECT_OPTIONS)+len(MOD_OPTIONS)+len(CONFIG_OPTIONS)+len(EXIT_OPTIONS)): EXIT_OPTIONS}
        print(mapped_options)
        print("Modpack Creator.\n------------------------------------------------")
        print("Please select an option from the following list:")
        while not done:
            self.main_menu_options()
            inp = input("Please enter your selected option: ")
            if not inp.isnumeric():
                print("Selection contains non-numbers.")
                continue
            inp = int(inp)
            if inp <= 0 or inp > len(PROJECT_OPTIONS) + len(MOD_OPTIONS) + len(EXIT_OPTIONS):
                print(f"Option {inp} is not a valid option.")
                return
            
            print(std.get_list(mapped_options, inp)[(inp-1)%len(std.get_list(mapped_options, inp))])
                # print(getattr(self, opt[inp-1].keys()))
        
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
        