from .modpack import Modpack
from .mod import Mod
import standard as std
import json
from typing import Optional, Dict, Any
from . import DEF_FILENAME
from .project_api import ProjectAPI  # Import the new ProjectAPI class

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

    mp: Modpack
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
        self.mp = Modpack(**kwargs)
        self.metadata.update({
            "loaded": True,
            "saved": False,
            "project_id": std.generate_id()
        })
        if not self.mp.check_compatibility():
            print("Invalid project created.")
            exit(1)

    def load_project(self, filename: str) -> None:
        """Loads project data from a file and initializes the modpack."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if not std.check_id(data["metadata"]["project_id"]):
                    std.eprint("[ERROR] Invalid project file.")
                    exit(1)

                self.metadata = data["metadata"]
                del data["metadata"]
                self.mp = Modpack(**data)
                
                if not self.mp.check_compatibility():
                    print("Invalid project loaded.")
                    exit(1)
        except Exception as e:
            std.eprint(f"[ERROR] Error processing file: {e}")
            exit(1)

    def save_project(self, filename: Optional[str] = None) -> None:
        """Saves the current project state to a file."""
        if filename is None:
            filename = DEF_FILENAME
        self.metadata["filename"] = filename
        self.metadata["saved"] = True
        project_data = self.mp.export_json()
        project_data["metadata"] = self.metadata
        with open(filename, 'w') as file:
            json.dump(project_data, file)

    def add_mod(self, name: str, versions: Dict[str, Any], mod_index: int) -> bool:
        """Adds a mod to the project's modpack."""
        project_info = self.api.get_project(name)
        if project_info is None:
            std.eprint(f"[ERROR] Could not find mod with name: {name}")
            return False
        
        mod_details = versions[mod_index]
        new_mod = Mod(
            mod_name=project_info["title"], 
            description=project_info["description"],
            mod_version=mod_details["version_number"],
            dependencies=mod_details["dependencies"],
            mc_versions=mod_details["game_versions"],
            client_side=project_info["client_side"],
            server_side=project_info["server_side"], 
            mod_loaders=mod_details["loaders"], 
            mod_id=mod_details["id"],
            project_id=mod_details["project_id"],
            date_published=mod_details["date_published"], 
            files=mod_details["files"]
        )
        self.mp.mod_list.append(new_mod)
        self.metadata["saved"] = False
        return True

    # The following methods are delegated to the ProjectAPI instance
    def parse_url(self, params: Dict[str, Any]) -> str:
        return self.api.parse_url(params)

    def is_slug_valid(self, slug_or_id: str) -> Optional[Dict[str, Any]]:
        return self.api.is_slug_valid(slug_or_id)

    def get_dependencies(self, project_name: str) -> Optional[Dict[str, Any]]:
        return self.api.get_dependencies(project_name)

    def search_project(self, **kwargs) -> Optional[Dict[str, Any]]:
        return self.api.search_project(**kwargs)

    def get_project(self, project_name: str) -> Optional[Dict[str, Any]]:
        return self.api.get_project(project_name)
    
    def list_versions(self, project_name: str, **kwargs) -> Optional[Dict[str, Any]]:
        return self.api.list_versions(project_name, **kwargs)
    
    def get_version(self, version_id: str) -> Optional[Dict[str, Any]]:
        return self.api.get_version(version_id)
    
    def get_versions(self, ids: str) -> Optional[Dict[str, Any]]:
        return self.api.get_versions(ids)
