import modpack.project as p
import standard as std
from simple_term_menu import TerminalMenu
from menu import ACCEPT



def load_project(project: p.Project) -> bool:
    """Load a project from a specified file, saving the current project if needed."""
    if project.metadata["loaded"] and not save_project(project):
        std.eprint("[ERROR] Could not save current project.")
        return False
    
    entries = std.get_project_files() + [None, "Enter filename"]
    project_list = TerminalMenu(
        title=f"Which project do you want to load?",
        menu_entries=entries,
        clear_screen=True
    )
    p_index = project_list.show()
    if p_index is None:
        return False

    if entries[p_index] == "Enter filename":
        filename = std.get_input("Please enter a project file: ")
        if filename is None:
            return False
    else:
        filename = entries[p_index]
    project.load_project(filename)
    return True

def create_project(project: p.Project) -> bool:
    """Create a new project with user-defined details and save it."""
    if project.metadata["loaded"] and not save_project(project):
        std.eprint("[ERROR] Could not save current project.")
        return False

    title = std.get_input("Please enter a project name: ")
    description = std.get_input("Please enter a description: ")
    mc_version = std.get_input("Please enter the project's Minecraft version: ")
    mod_loader = std.get_input("Please enter the project's modloader: ")

    if any(value is None for value in [title, description, mc_version, mod_loader]):
        return False

    project.create_project(
        title=title,
        description=description,
        mc_version=mc_version,
        mod_loader=mod_loader,
    )
    return True

def save_project(project: p.Project) -> bool:
    """Save the current project to a file, optionally with a new filename."""
    if not project.metadata["saved"]:
        if std.get_input("Do you want to save the project? y/n: ") == ACCEPT:
            if std.get_input("Do you want to save the project to a new file? y/n: ") == ACCEPT:
                filename = std.get_input("Please enter the filename to save to: ")
                if filename is None:
                    return False
                project.save_project(filename)
            else:
                project.save_project(project.metadata["filename"])
            project.metadata["saved"] = True
    return True

# TODO Add more info when multiple mods are selected
def search_mods(project: p.Project) -> bool:
    """Search for mods based on user input and add selected mods to the project."""
    query = std.get_input("Please enter a term to search for: ")
    if not query:
        return False

    kwargs = {
        "query": query,
        "facets": [
            [f"categories:{project.mp.mod_loader}"],
            [f"versions:{project.mp.mc_version}"]
        ],
        "limit": 200
    }

    if std.get_input("Do you want to enter additional facets? y/n: ") == ACCEPT:
        facets = std.get_input("Enter the facets you want to search with (e.g., modloader(s), minecraft version(s)): ")
        if facets is None:
            std.eprint("[ERROR] No facets given.")
            return False
        temp = [[f"{key}:{item}" for item in value.split()] for key, value in zip(["categories", "versions"], facets.split(','))]
        kwargs["facets"] = [item for facet in temp for item in facet] + ["project_type:mod"]

    results = project.search_project(**kwargs)

    while True:
        result_list = TerminalMenu(
            title="Which entries do you want to add? Select one option to see its details.",
            menu_entries=[f'{mod["title"]}: ' for mod in results["hits"]],
            multi_select=True,
            clear_screen=True
        )
        mod_indices = result_list.show()
        if mod_indices is None:
            return False
        
        if len(mod_indices) == 1:
            selected_mod = results["hits"][mod_indices[0]]
            if input(f'''{selected_mod["title"]}
Client side: {selected_mod["client_side"]}
Server side: {selected_mod["server_side"]}

{selected_mod["description"]}
Do you want to add this mod to the current project? y/n ''') != ACCEPT:
                continue
        for i in mod_indices:
            res = add_mods(project, results["hits"][i]["slug"])
        return res


def add_mods_input(project: p.Project) -> bool:
    """Add multiple mods to the current project based on user input."""
    names = std.get_input("Please enter mod slugs or IDs (e.g., name1 name2 ...): ")
    if not names:
        return False
    
    return all(add_mods(project, name) for name in names.split())


# TODO: Ask for user confirmation when selecting mod to add 
def add_mods(project: p.Project, name: str) -> bool:
    """Add a mod to the current project by its name."""
    if not project.is_slug_valid(name):
        std.eprint("[ERROR] Invalid mod name/id.")
        return False

    versions = project.list_versions(name, loaders=[project.mp.mod_loader], game_versions=[project.mp.mc_version])
    if versions is None:
        std.eprint(f"[ERROR] No mod called {name} found.")
        return False
    while True:
        version_list = TerminalMenu(
            title=f"Which version of {name} do you want to add?",
            menu_entries=[f'{version["name"]}: minecraft version(s): {version["game_versions"]}, {version["version_type"]}' for version in versions],
            clear_screen=True
        )
        mod_index = version_list.show()
        if mod_index is None:
            return False

        if input(f'{versions[mod_index]["name"]}:\n{versions[mod_index]["changelog"]}\nDo you want to add this mod to the current project? y/n ') is ACCEPT:
            return project.add_mod(name, versions, mod_index)


def remove_mods(project: p.Project, indices) -> bool:
    """Remove mods from the current project based on their indices."""
    if indices is None:
        return False

    for i in sorted(indices, reverse=True):
        del project.mp.mod_list[i]

    project.metadata["saved"] = False
    return True

def change_project_attribute(project: p.Project, attribute: str, prompt: str) -> bool:
    """Change a project attribute based on user input."""
    new_value = std.get_input(prompt)
    if not new_value:
        return False

    setattr(project.mp, attribute, new_value)
    project.metadata["saved"] = False
    return True

def change_project_title(project: p.Project) -> bool:
    """Change the name of the current project."""
    return change_project_attribute(project, "title", "Please enter a new name: ")

def change_project_description(project: p.Project) -> bool:
    """Change the description of the current project."""
    return change_project_attribute(project, "description", "Please enter a new description: ")

def change_project_version(project: p.Project) -> bool:
    """Change the version of the current project."""
    return change_project_attribute(project, "build_version", "Please enter a new version: ")

def change_project_loader(project: p.Project) -> bool:
    """Change the modloader of the current project."""
    return change_project_attribute(project, "mod_loader", "Please enter a new modloader: ")

def change_mc_version(project: p.Project) -> bool:
    """Change the Minecraft version of the current project."""
    return change_project_attribute(project, "mc_version", "Please enter a new Minecraft version: ")

def exit_program(project: p.Project) -> bool:
    """Exit the program, prompting to save the project if necessary."""
    return save_project(project) if not project.metadata["saved"] else True

def placeholder() -> bool:
    """Placeholder function that always returns `True`."""
    return True
