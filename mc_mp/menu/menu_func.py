import modpack.project as p
import modpack.mod as mod
import standard as std
from simple_term_menu import TerminalMenu
# 
# Project options
# 
def load_project(project: p.Project) -> bool:
    """Loads a project"""
    filename = str(input("Please enter a project filename: "))
    if not filename.isascii() or len(filename) == 0:
        std.eprint("[ERROR] Filename contains non-ASCII characters or is empty.")
        return False
    
    project.load_project(filename)
    return True

def create_project(project: p.Project) -> bool:
    """Creates a project"""
    if project.metadata["loaded"]:
        if not save_project(project):
            std.eprint("[ERROR] Could not save current project.")
            return False
        
    title = str(input("Please enter a project name: "))
    description = str(input("Please enter a description: "))
    mc = str(input("Please enter the projects minecraft version: "))
    modloader = str(input("Please enter the projects modloader: "))
    allow_alpha_beta = str(input("Allow alpha/beta mods? y/n "))

    if not (title.isascii() and description.isascii() and mc.isascii() and modloader.isascii() and allow_alpha_beta.isascii()):
        std.eprint("[ERROR] Input contains non-ASCII characters.")
        return False
    project.create_project(title=title, description=description, mc_version=mc, mod_loader=modloader, flags={"allow_alpha_beta": allow_alpha_beta == 'y'})
    return True

def save_project(project: p.Project) -> bool:
    """Saves a project"""
    if not project.metadata["saved"]:
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
                project.save_project(project.metadata["filename"])
            project.metadata["saved"] = True
    return True

# 
# Modpack options
# 
def search_mods(project: p.Project) -> bool:
    """Enter a (list of) mod(s) to add"""
    query = str(input("Please enter a term to search for: "))
    if not query.isascii() or len(query) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    f = str(input("Do you want to enter additional filters? y/n "))
    if f.isascii() and f == 'y':
        facets = str(input("Enter the facets you want to search with: (modloader, minecraft version, client side, server side) "))
        print(facets)
    
    results = project.search_project(query=query, facets=[[f"categories:{project.mp.mod_loader}"], [f"versions:{project.mp.mc_version}"], ["project_type:mod"], ])
    print(results)
    return True

def add_mods(project: p.Project) -> bool:
    """Adds some mod(s) to the current project"""
    names = str(input("Please enter a mod slug or id: [name1 name2 ...] "))
    if not names.isascii() or len(names) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    names = names.split()
    for name in names:
        versions = project.list_versions(name, loaders=[project.mp.mod_loader], game_versions=[project.mp.mc_version])
        if versions is None:
            std.eprint(f"[ERROR] No mod called {name} found.")
        version_list = TerminalMenu([f'{version["name"]}: minecraft version(s): {version["game_versions"]}, {version["version_type"]}' for version in versions], 
                                    clear_screen=False)
        mod_index = version_list.show()
        if mod_index is None:
            return False
        
        print(f'{versions[mod_index]["name"]}:\n{versions[mod_index]["changelog"]}')
        inp = str(input("Do you want to add this mod to the current project? y/n "))
        if inp.isascii() and inp == 'y':
            project_info = project.get_project(name)
            print(project_info)
            print(versions[mod_index])
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

def add_mods_from_file(project: p.Project) -> bool:
    """Adds some mod(s) to the current project"""
    # TODO
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
    inp = str(input("Please enter a new name: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.name = inp
    project.metadata["saved"] = False
    return True

def change_project_version(project: p.Project) -> bool:
    """Change the version of the current project"""
    inp = str(input("Please enter a new version: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.build_version = inp
    project.metadata["saved"] = False
    return True

def change_project_loader(project: p.Project) -> bool:
    """Change the modloader of the current project"""
    inp = str(input("Please enter a new modloader: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.mod_loader = inp
    project.metadata["saved"] = False
    return True

def change_mc_version(project: p.Project) -> bool:
    """Change the minecraft version of the current project"""
    inp = str(input("Please enter a new minecraft version: "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.mc_version = inp
    project.metadata["saved"] = False
    return True

def allow_alpha_beta(project: p.Project) -> bool:
    """Change if mods in alpha or beta are allowd"""
    inp = str(input("Allow alpha/beta mods? y/n "))
    if not inp.isascii() or len(inp) == 0:
        std.eprint("[ERROR] Name contains non-ASCII characters or is empty.")
        return False
    
    project.mp.flags["allow_alpha_beta"] = inp == 'y'
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