# 
# Project options
# 
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

# 
# Modpack options
# 
def add_mods(project) -> bool:
    """Adds some mod(s) to the current project"""
    
    return True

def remove_mods(project) -> bool:
    """Removes some mod(s) from the current project"""
    
    return True

    
# 
# Config options
#

def change_project_name(project) -> bool:
    """Change the name of the current project"""
    
    return True

def change_project_version(project) -> bool:
    """Change the version of the current project"""
    
    return True

def change_project_loader(project) -> bool:
    """Change the modloader of the current project"""
    
    return True

def change_mc_version(project) -> bool:
    """Change the minecraft version of the current project"""
    
    return True



# 
# Misc options
#
def get_config_menu() -> bool:
    return True


def exit_program(project) -> bool:
    """Exits the program"""

    if not project.saved:
        inp = str(input("Do you want to save the project? y/n"))
        
        if inp == 'y':
            project.save_project(project.filename)
            print("Project saved.")
    return True