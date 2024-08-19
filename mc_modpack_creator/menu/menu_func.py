import modpack.project as proj
# 
# Project options
# 
def load_project(project: proj.Project) -> bool:
    """Loads a project"""
    filename = str(input("Please enter a project filename: "))
    if not filename.isascii() or len(filename) == 0:
        print("Filename contains non-ASCII characters or is empty.")
        return False
    
    project.load_project(filename)
    return True

def create_project(project: proj.Project) -> bool:
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

def save_project(project: proj.Project) -> bool:
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
def add_mods(project: proj.Project) -> bool:
    """Adds some mod(s) to the current project"""
    
    return True

def remove_mods(project: proj.Project, indices) -> bool:
    """Removes some mod(s) from the current project"""
    if indices is None:
        return False
    for i in sorted(indices, reverse=True):
        del project.mp.mod_list[i]
    return True

    
# 
# Config options
#

def change_project_name(project: proj.Project) -> bool:
    """Change the name of the current project"""
    name = str(input("Please enter a new name: "))
    if not name.isascii() or len(name) == 0:
        print("Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.name = name
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
        return save_project(project)
    return True