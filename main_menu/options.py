class options:
    def load_project(self) -> bool:
        """Loads a project"""
        filename = str(input("Please enter a project filename: "))
        if not filename.isalnum():
            print("Filename contains non-ASCII characters.")
            return False
        
        return True
    def create_project(self) -> bool:
        """Creates a project"""
        name = str(input("Please enter a project name: "))
        if not name.isalnum():
            print("Filename contains non-ASCII characters.")
            return False
        
        return True
    def save_project(self) -> bool:
        """Saves a project"""
        filename = str(input("Please enter the filename to save to: "))
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