import requests
import json
from typing import Optional, Dict, Any
import modpack.modpack as modpack
import modpack.mod as mod
import standard as std
from . import API_BASE, HEADERS, DEF_FILENAME


class Project:
    """
    Manages projects related to modpacks, including mod information and API interactions.

    Attributes
    ----------
    mp : modpack.Modpack
        An instance of the `Modpack` class.
    metadata : dict
        Metadata about the project, including loading and saving status, filename, and project ID.

    Methods
    -------
    __init__(**kwargs)
        Initializes a new `Project` instance.
    create_project(**kwargs)
        Creates a new project and updates metadata.
    load_project(filename: str)
        Loads project data from a file and initializes the modpack.
    save_project(filename: Optional[str] = None)
        Saves the current project state to a file.
    add_mod(name: str, versions: Dict[str, Any], mod_index: int) -> bool
        Adds a mod to the project's modpack.
    rm_mod()
        Placeholder for removing a mod from the project.
    parse_url(params: Dict[str, Any]) -> str
        Converts a dictionary to a URL query string.
    is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]
        Checks if the project name or ID exists on Modrinth.
    get_dependencies(project_name: str) -> Optional[Dict[str, Any]]
        Retrieves all dependencies of a given project.
    search_project(**kwargs) -> Optional[Dict[str, Any]]
        Searches for projects using various filters and sorting options.
    get_project(project_name: str) -> Optional[Dict[str, Any]]
        Retrieves information about a specific project.
    list_versions(project_name: str, **kwargs) -> Optional[Dict[str, Any]]
        Lists versions of a given project with optional filtering.
    get_version(version_id: str) -> Optional[Dict[str, Any]]
        Retrieves information about a specific version by ID.
    get_versions(ids: str) -> Optional[Dict[str, Any]]
        Retrieves information about multiple versions by their IDs.
    """

    mp: modpack.Modpack
    metadata: Dict[str, Any] = {
        "loaded": False,
        "saved": True,
        "filename": "project1.json",
        "project_id": None
    }
    
    def __init__(self, **kwargs) -> None:
        """Initializes a Project instance."""
        pass

    def create_project(self, **kwargs) -> None:
        """Creates a new project and updates metadata."""
        self.mp = modpack.Modpack(**kwargs)
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
                self.mp = modpack.Modpack(**data)
                
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
        project_info = self.get_project(name)
        if project_info is None:
            std.eprint(f"[ERROR] Could not find mod with name: {name}")
            return False
        
        mod_details = versions[mod_index]
        new_mod = mod.Mod(
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

    def parse_url(self, params: Dict[str, Any]) -> str:
        """Converts a dictionary to a URL query string."""
        return '&'.join(f'{key}={value}' for key, value in params.items()).replace('\'', '\"')

    def is_slug_valid(self, slug_or_id: str) -> Optional[Dict[str, Any]]:
        """Checks if the given project name or ID exists on Modrinth."""
        response = requests.get(f"{API_BASE}/project/{slug_or_id}/check", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    def get_dependencies(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves all dependencies of a given project."""
        if self.is_slug_valid(project_name) is None:
            return None
        
        response = requests.get(f"{API_BASE}/project/{project_name}/dependencies", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    def search_project(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Searches for projects using various filters and sorting options."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        response = requests.get(f"{API_BASE}/search", params=self.parse_url(params), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    def get_project(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific project."""
        if self.is_slug_valid(project_name) is None:
            return None

        response = requests.get(f"{API_BASE}/project/{project_name}", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    
    def list_versions(self, project_name: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Lists versions of a given project with optional filtering."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        if self.is_slug_valid(project_name) is None:
            return None

        response = requests.get(f"{API_BASE}/project/{project_name}/version", params=self.parse_url(params), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_version(self, version_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific version by ID."""
        response = requests.get(f"{API_BASE}/version/{version_id}", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_versions(self, ids: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about multiple versions by their IDs."""
        params = {'ids': ids}
        response = requests.get(f"{API_BASE}/versions", params=self.parse_url(params), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
