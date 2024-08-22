import modpack.project as proj
import standard as std
import ast
# 
# Project options
# 
def load_project(project: proj.Project) -> bool:
    """Loads a project"""
    filename = str(input("Please enter a project filename: "))
    if not filename.isascii() or len(filename) == 0:
        std.eprint("[ERROR] Filename contains non-ASCII characters or is empty.")
        return False
    
    project.load_project(filename)
    return True

def create_project(project: proj.Project) -> bool:
    """Creates a project"""
    if project.loaded:
        if not save_project(project):
            std.eprint("[ERROR] Could not save current project.")
            return False
        
    name = str(input("Please enter a project name: "))
    description = str(input("Please enter a description: "))
    mc = str(input("Please enter the projects minecraft version: "))
    modloader = str(input("Please enter the projects modloader: "))

    if not (name.isascii() and description.isascii() and mc.isascii() and modloader.isascii()):
        std.eprint("[ERROR] Input contains non-ASCII characters.")
        return False
    project.create_project(name=name, description=description, mc_version=mc, mod_loader=modloader)
    return True

def save_project(project: proj.Project) -> bool:
    """Saves a project"""
    if not project.saved:
        inp = str(input("Do you want to save the project? y/n: "))
        if inp == 'y': 
            inp = str(input("Do you want to save the project to a new file? y/n: "))
            if inp == 'y':
                filename = str(input("Please enter the filename to save to: "))
                if not filename.isascii():
                    std.eprint("[ERROR] Filename contains non-ASCII characters.")
                    return False
                project.save_project(filename)
            else: 
                project.save_project(project.filename)
            project.saved = True
    return True

# 
# Modpack options
# 
def search_mods(project: proj.Project) -> bool:
    """Search for a (list of) mod(s) to add"""
    names = str(input("Please enter a mod name or id: [name/id or name1 name2 ...] "))
    if not names.isascii() or len(names) == 0:
        std.eprint("[ERROR] Filename contains non-ASCII characters or is empty.")
        return False
    names = names.split()
    print(names)
    return True

def add_mods(project: proj.Project) -> bool:
    """Adds some mod(s) to the current project"""
    # TODO
    return True

def add_mods_from_file(project: proj.Project) -> bool:
    """Adds some mod(s) to the current project"""
    # TODO
    return True

def remove_mods(project: proj.Project, indices) -> bool:
    """Removes some mod(s) from the current project"""
    if indices is None:
        return False
    for i in sorted(indices, reverse=True):
        del project.mp.mod_list[i]
    project.saved = False
    return True
    
# 
# Config options
#

def change_project_name(project: proj.Project) -> bool:
    """Change the name of the current project"""
    inp = str(input("Please enter a new name: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.name = inp
    project.saved = False
    return True

def change_project_version(project: proj.Project) -> bool:
    """Change the version of the current project"""
    inp = str(input("Please enter a new version: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.build_version = inp
    project.saved = False
    return True

def change_project_loader(project: proj.Project) -> bool:
    """Change the modloader of the current project"""
    inp = str(input("Please enter a new modloader: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.mod_loader = inp
    project.saved = False
    return True

def change_mc_version(project: proj.Project) -> bool:
    """Change the minecraft version of the current project"""
    inp = str(input("Please enter a new minecraft version: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.mc_version = inp
    project.saved = False
    return True

# 
# Misc options
#
def get_config_menu() -> bool:
    """"Placeholder"""
    return True


def exit_program(project) -> bool:
    """Exits the program"""
    if not project.saved:
        return save_project(project)
    return True