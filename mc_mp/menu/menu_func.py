import modpack.project as p
import modpack.mod as mod
import standard as std
from simple_term_menu import TerminalMenu
from menu import ACCEPT
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
    """Search for new mods"""
    query = std.get_input("Please enter a term to search for: ")
    if query is None or len(query) == 0:
        return False
    
    f = std.get_input("Do you want to enter additional facets? y/n ")
    if f == ACCEPT:
        facets = std.get_input("Enter the facets you want to search with: [modloader(s) ..., minecraft version(s) ...: ")
        if facets is None:
            std.eprint("[ERROR] No facets given.")
            return False
        temp = [[f"{key}:{item}" for item in value.split()] for key, value in zip(["categories", "versions"], facets.split(','))]
        facets = [[item] for facet in temp for item in facet]; facets.append(["project_type:mod"])
        print(facets)
        # , client side (required/optional/unsupported), server side (required/optional/unsupported)]
        results = project.search_project(query=query, facets=facets)
        result_list = TerminalMenu([f'{mod["name"]}: ' for mod in results], 
                                    clear_screen=False)
        mod_index = result_list.show()
        if mod_index is None:
            return False
        return True
    results = project.search_project(query=query)
    print(results)
    return True

def add_mods(project: p.Project) -> bool:
    """Add some mod(s) to the current project"""
    names = std.get_input("Please enter a mod slug or id: [name1 name2 ...]: ")
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
            if not project.add_mod(name, versions, mod_index):
                std.eprint(f"[ERROR] Could not find {name}.")
                continue
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