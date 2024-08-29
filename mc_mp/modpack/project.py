from .modpack import Modpack
from .mod import Mod
import standard as std
import json
import os
from typing import Optional, Dict, Any
from . import DEF_FILENAME, ACCEPT
from .project_api import ProjectAPI  # Import the new ProjectAPI 

class Project:
    """
    Manages projects related to modpacks, including mod information and API interactions.

    Attributes
    ----------
    mp : Modpack
        An instance of the Modpack class representing the modpack for the project.
    metadata : dict
        A dictionary containing project metadata with the following keys:
        - 'loaded' (bool): Whether the project is loaded.
        - 'saved' (bool): Whether the project is saved.
        - 'filename' (str): The filename of the project file.
        - 'project_id' (Optional[str]): The ID of the project.

    Methods
    -------
    __init__(**kwargs)
        Initializes a Project instance and instantiates the ProjectAPI class.
    
    create_project(**kwargs)
        Creates a new project, updates metadata, and checks modpack compatibility.

    load_project(filename: str)
        Loads project data from a file, initializes the modpack, and checks compatibility.

    save_project(filename: Optional[str] = None)
        Saves the current project state to a file, using a default filename if none is provided.

    add_mod(name: str, versions: Dict[str, Any], mod_index: int) -> bool
        Adds a mod to the project's modpack based on the provided name and version index.

    parse_url(params: Dict[str, Any]) -> str
        Parses a URL using the ProjectAPI instance.

    is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]
        Checks if a slug or ID is valid using the ProjectAPI instance.

    get_dependencies(project_name: str) -> Optional[Dict[str, Any]]
        Retrieves dependencies for a project using the ProjectAPI instance.

    search_project(**kwargs) -> Optional[Dict[str, Any]]
        Searches for a project using the ProjectAPI instance.

    get_project(project_name: str) -> Optional[Dict[str, Any]]
        Retrieves project details using the ProjectAPI instance.

    list_versions(project_name: str, **kwargs) -> Optional[Dict[str, Any]]
        Lists versions of a project using the ProjectAPI instance.

    get_version(version_id: str) -> Optional[Dict[str, Any]]
        Retrieves details of a specific version using the ProjectAPI instance.

    get_versions(ids: str) -> Optional[Dict[str, Any]]
        Retrieves details of multiple versions using the ProjectAPI instance.
    """

    modpack: Modpack
    api: ProjectAPI
    metadata: Dict[str, Any] = {
        "loaded": False,
        "saved": True,
        "filename": "project1.json",
        "project_id": None
    }

    def __init__(self, **kwargs) -> None:
        """Initializes a Project instance."""
        self.api = ProjectAPI()  # Instantiate the ProjectAPI class

    def create_project(self, **kwargs) -> None:
        """Creates a new project and updates metadata."""
        self.modpack = Modpack(**kwargs)
        self.metadata.update({
            "loaded": True,
            "saved": False,
            "project_id": std.generate_project_id()
        })
        if not self.modpack.check_compatibility():
            std.eprint("[ERROR]: Invalid project created.")
            exit(1)
        

    def load_project(self, filename: str) -> bool:
        """Loads project data from a file and initializes the modpack."""
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                if not std.is_valid_project_id(data["metadata"]["project_id"]):
                    std.eprint("[ERROR] Invalid project file.")
                    exit(1)

                self.metadata = data["metadata"]; del data["metadata"]
                self.modpack = Modpack(**data)
                
                if not self.modpack.check_compatibility():
                    print("Invalid project loaded.")
                    exit(1)
            self.metadata["loaded"] = True
            self.metadata["saved"] = True
            return True
        return False

    def save_project(self, filename: Optional[str]=DEF_FILENAME) -> bool:
        """Saves the current project state to a file."""
        if filename:
            self.metadata["filename"] = filename
        if not self.metadata["filename"]:
            return False

        project_data = self.modpack.export_json(); project_data["metadata"] = self.metadata
        with open(self.metadata["filename"], 'w') as file:
            json.dump(project_data, file, indent=4)
        self.metadata["saved"] = True
        return True


    def add_mod(self, name: str, version: dict, project_info: dict, index: int=-1) -> bool:
        """Adds a mod to the project's modpack."""
        if any([project_info, version]) is None:
            std.eprint(f"[ERROR] Could not find mod with name: {name}")
            return False
        
        self.modpack.mod_data.insert(index, Mod(
            title=project_info["title"],
            description=project_info["description"],
            name=version["name"], 
            changelog=version["changelog"], 
            version_number=version["version_number"],
            dependencies=version["dependencies"],
            mc_versions=version["game_versions"],
            mod_loaders=version["loaders"], 
            id=version["id"],
            project_id=version["project_id"],
            date_published=version["date_published"], 
            files=version["files"]
        ))
        self.metadata["saved"] = False
        return True
    
    def rm_mod(self, index: int) -> bool:
        try:
            del self.modpack.mod_data[index]
            self.metadata["saved"] = False
            return True
        except:
            return False

    def update_mod(self, new_version: dict, index: int, project_info: dict) -> bool:
        name = self.modpack.mod_data[index].project_id
        self.rm_mod(index); self.add_mod(name, new_version, project_info, index)
    
    def list_projects(self) -> list[str]:
        valid_projects: list[str] = []
        for filename in std.get_project_files():
            try:
                with open(filename, 'r') as file:
                    data = json.load(file)
                    if std.is_valid_project_id(data["metadata"]["project_id"]):
                        valid_projects.append(f'{filename}: {data["title"]}, {data["description"]}')
            except:
                continue
        return valid_projects
    
    def list_mods(self) -> list[str]:
        if self.metadata["loaded"]:
            return [f'{m}:\n\t{d}' for m,d in zip(self.modpack.get_mod_list_names(), self.modpack.get_mod_list_descriptions())]
        return None