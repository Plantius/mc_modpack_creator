from .modpack import Modpack
from .mod import Mod
import standard as std
import json, os
from typing import Optional, Dict, Any
from . import DEF_FILENAME, ACCEPT
from .project_api import ProjectAPI
import concurrent.futures as cf
from dateutil import parser
import asyncio


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

    def is_mod_installed(self, id: str) -> int:
        return std.get_index([m.project_id for m in self.modpack.mod_data], id)
    
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

    async def search_mods(self, **kwargs) -> dict:
        """Search for mods using the API."""
        return await self.api.search_project(**kwargs)
    
    
    async def add_mod(self, name: str, version: dict, project_info: dict, index: int=0) -> bool:
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

    async def update_mod(self, selected_index) -> bool:
        ids = [id.project_id for id in self.modpack.mod_data]
        mods_versions_info_all = await self.fetch_mods_by_ids(ids)
        if not any(mods_versions_info_all):
            std.eprint("[ERROR] Could not find mods.")            
            return False
            
        latest_version_all = [versions[0] for versions in [p["versions"] for p in mods_versions_info_all] if versions is not None]
        project_info_all = [info["project_info"] for info in mods_versions_info_all]
        for index, latest_version, project_info in zip(selected_index, latest_version_all, project_info_all):
            new_mod_date = parser.parse(latest_version["date_published"])
            current_mod_date = parser.parse(self.modpack.mod_data[index].date_published)
            if new_mod_date > current_mod_date:
                inp = std.get_input(f"There is a newer version available for {self.modpack.mod_data[index].name}, do you want to upgrade? y/n {self.modpack.mod_data[index].version_number} -> {latest_version['version_number']} ")
                if inp == ACCEPT:
                    name = self.modpack.mod_data[index].project_id
                    self.rm_mod(index); self.add_mod(name, latest_version, project_info, index)
            print(f"{self.modpack.get_mods_name_ver()[index]} is up to date")
    
    def list_projects(self) -> list[str]:
        valid_projects: list[str] = []; 
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
    
    async def fetch_mods_by_ids(self, ids: list[str]) -> list[dict]:
        ids = [id for id in ids if not self.is_mod_installed(id)]
        tasks: list = []; mods_ver_info: list[dict] = []
        for id in ids:
            tasks.append(self.api.list_versions(id=id, loaders=[self.modpack.mod_loader], game_versions=[self.modpack.mc_version]))
            tasks.append(self.api.get_project(id))
        
        res = await asyncio.gather(*tasks)
        versions_all = res[::2]; project_info_all = res[1::2]
        for versions, project_info in zip(versions_all, project_info_all):
            if versions and project_info:
                mods_ver_info.append({"project_info": project_info,
                                      "versions": versions})
        return mods_ver_info