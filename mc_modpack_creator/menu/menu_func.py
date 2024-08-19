# 
# Project options
# 
def load_project(project) -> bool:
    """Loads a project"""
    filename = str(input("Please enter a project filename: "))
    if not filename.isascii():
        print("Filename contains non-ASCII characters.")
        return False
    
    project.load_project(filename)
    return True

def create_project(project) -> bool:
    """Creates a project"""
    name = str(input("Please enter a project name: "))
    description = str(input("Please enter a description: "))
    mc = str(input("Please enter the projects minecraft version: "))
    modloader = str(input("Please enter the projects modloader: "))

    if not (name.isascii() and description.isascii() and mc.isascii() and modloader.isascii()):
        print("Input contains non-ASCII characters.")
        return False
    project.create_project(name=name, description=description, mc_version=mc, mod_loader=modloader)
    return True

def save_project(project) -> bool:
    """Saves a project"""
    if not project.saved:
        inp = str(input("Do you want to save the project to a new file? y/n: "))
        if inp == 'y':
            filename = str(input("Please enter the filename to save to: "))
            if not filename.isascii():
                print("Filename contains non-ASCII characters.")
                return False
            project.save_project(filename)
        else: 
            project.save_project(project.filename)
        project.saved = True
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
        inp = str(input("Do you want to save the project? y/n: "))
        if inp == 'y':
            project.save_project(project.filename)
    return True