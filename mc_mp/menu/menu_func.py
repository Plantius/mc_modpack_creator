import modpack.project as p
import modpack.mod as mod
import standard as std
from simple_term_menu import TerminalMenu
from menu import ACCEPT, REJECT
# 
# Project options
# 
def load_project(project: p.Project) -> bool:
    """Loads a project"""
    if project.metadata["loaded"]:
        if not save_project(project):
            std.eprint("[ERROR] Could not save current project.")
            return False
    filename = std.get_input("Please enter a project file: ")
    if filename is None:
        return False
    
    project.load_project(filename)
    return True

def create_project(project: p.Project) -> bool:
    """Creates a project"""
    if project.metadata["loaded"]:
        if not save_project(project):
            std.eprint("[ERROR] Could not save current project.")
            return False
        
    title = std.get_input("Please enter a project name: ")
    description = std.get_input("Please enter a description: ")
    mc = std.get_input("Please enter the projects minecraft version: ")
    modloader = std.get_input("Please enter the projects modloader: ")
    allow_alpha_beta = std.get_input("Allow alpha/beta mods? y/n ")

    if title is None or description is None or mc is None or modloader is None or allow_alpha_beta is None:
        return False
    
    project.create_project(title=title, description=description, mc_version=mc, mod_loader=modloader, flags={"allow_alpha_beta": allow_alpha_beta == ACCEPT})
    return True

def save_project(project: p.Project) -> bool:
    """Saves a project"""
    if not project.metadata["saved"]:
        inp = std.get_input("Do you want to save the project? y/n: ")
        if inp == ACCEPT: 
            inp = std.get_input("Do you want to save the project to a new file? y/n: ")
            if inp == ACCEPT:
                filename = std.get_input("Please enter the filename to save to: ")
                if filename is None:
                    return False
                project.save_project(filename)
            else: 
                project.save_project(project.metadata["filename"])
            project.metadata["saved"] = True
    return True

# 
# Modpack options
# 
def search_mods(project: p.Project) -> bool:
    """Enter a (list of) mod(s) to add"""
    query = std.get_input("Please enter a term to search for: ")
    if query is None or len(query) == 0:
        return False
    
    f = std.get_input("Do you want to enter additional filters? y/n ")
    if f == ACCEPT:
        facets = std.get_input("Enter the facets you want to search with: (modloader, minecraft version, client side, server side) ")
        if facets is None:
            return False
    
    results = project.search_project(query=query, facets=[[f"categories:{project.mp.mod_loader}"], [f"versions:{project.mp.mc_version}"], ["project_type:mod"], ])
    print(results)
    return True

def add_mods(project: p.Project) -> bool:
    """Adds some mod(s) to the current project"""
    names = std.get_input("Please enter a mod slug or id: [name1 name2 ...] ")
    if names is None or len(names) == 0:
        return False
    names = names.split()
    for name in names:
        if not project.is_slug_valid(name):
            std.eprint("[ERROR] Invalid project name/id.")
            continue
        versions = project.list_versions(name, loaders=[project.mp.mod_loader], game_versions=[project.mp.mc_version])
        if versions is None:
            std.eprint(f"[ERROR] No mod called {name} found.")
        version_list = TerminalMenu([f'{version["name"]}: minecraft version(s): {version["game_versions"]}, {version["version_type"]}' for version in versions], 
                                    clear_screen=False)
        mod_index = version_list.show()
        if mod_index is None:
            return False
        
        print(f'{versions[mod_index]["name"]}:\n{versions[mod_index]["changelog"]}')
        inp = std.get_input("Do you want to add this mod to the current project? y/n ")
        if inp == ACCEPT:
            project_info = project.get_project(name)
            project.mp.mod_list.append(mod.Mod(mod_name=project_info["title"], 
                                               description=project_info["description"],
                                               mod_version=versions[mod_index]["version_number"],
                                               dependencies=versions[mod_index]["dependencies"],
                                               mc_versions=versions[mod_index]["game_versions"],
                                               client_side=project_info["client_side"],
                                               server_side=project_info["server_side"], 
                                               mod_loaders=versions[mod_index]["loaders"], 
                                               mod_id=versions[mod_index]["id"],
                                               project_id=versions[mod_index]["project_id"],
                                               date_published=versions[mod_index]["date_published"], 
                                               files=versions[mod_index]["files"]))
            project.metadata["saved"] = False
    return True


def remove_mods(project: p.Project, indices) -> bool:
    """Removes some mod(s) from the current project"""
    if indices is None:
        return False
    for i in sorted(indices, reverse=True):
        del project.mp.mod_list[i]
    project.metadata["saved"] = False
    return True
    
# 
# Config options
#

def change_project_name(project: p.Project) -> bool:
    """Change the name of the current project"""
    inp = std.get_input("Please enter a new name: ")
    if inp is None or len(inp) == 0:
        return False
    
    project.mp.name = inp
    project.metadata["saved"] = False
    return True

def change_project_version(project: p.Project) -> bool:
    """Change the version of the current project"""
    inp = std.get_input("Please enter a new version: ")
    if inp is None or len(inp) == 0:
        return False
    
    project.mp.build_version = inp
    project.metadata["saved"] = False
    return True

def change_project_loader(project: p.Project) -> bool:
    """Change the modloader of the current project"""
    inp = std.get_input("Please enter a new modloader: ")
    if inp is None or len(inp) == 0:
        return False
    
    project.mp.mod_loader = inp
    project.metadata["saved"] = False
    return True

def change_mc_version(project: p.Project) -> bool:
    """Change the minecraft version of the current project"""
    inp = std.get_input("Please enter a new minecraft version: ")
    if inp is None or len(inp) == 0:
        return False
    
    project.mp.mc_version = inp
    project.metadata["saved"] = False
    return True

def allow_alpha_beta(project: p.Project) -> bool:
    """Change if mods in alpha or beta are allowd"""
    inp = std.get_input("Allow alpha/beta mods? y/n ")
    if inp is None or len(inp) == 0:
        return False
    
    project.mp.flags["allow_alpha_beta"] = inp == ACCEPT
    project.metadata["saved"] = False
    return True

# 
# Misc options
#

def exit_program(project) -> bool:
    """Exits the program"""
    if not project.metadata["saved"]:
        return save_project(project)
    return True

def placeholder() -> bool:
    """"Placeholder"""
    return True