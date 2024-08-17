def load_project() -> bool:
    """Loads a project"""
    filename = str(input("Please enter a project filename: "))
    if not filename.isalnum():
        print("Filename contains non-ASCII characters.")
        return False
    
    return True
def create_project() -> bool:
    """Creates a project"""
    name = str(input("Please enter a project name: "))
    if not name.isalnum():
        print("Filename contains non-ASCII characters.")
        return False
    
    return True
def save_project() -> bool:
    """Saves a project"""
    filename = str(input("Please enter the filename to save to: "))
    if not filename.isalnum():
        print("Filename contains non-ASCII characters.")
        return False
    
    return True

def exit_program(project) -> bool:
    """Exits the program"""
    print("Exiting program.")
    if not project.saved:
        inp = str(input("Do you want to save the project? y/n"))
        
        if inp == 'y':
            project.save_project(project.filename)
            print("Project saved.")
    return True