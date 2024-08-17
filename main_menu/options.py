class options:
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