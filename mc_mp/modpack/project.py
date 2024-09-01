"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/project.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from .modpack import Modpack
from .mod import Mod
import standard as std
import json, os
from typing import Optional, Dict, Any
from . import DEF_FILENAME, ACCEPT
from .project_api import ProjectAPI
from dateutil import parser
import asyncio


class Project:
    """
    Manages projects, including modpacks, mod information, and API interactions.
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
        """Initializes a Project instance and ProjectAPI."""
        self.api = ProjectAPI()

    def is_mod_installed(self, id: str) -> int:
        """Checks if a mod is installed by ID and returns its index."""
        result = std.get_index([m.project_id for m in self.modpack.mod_data], id)
        return result
    
    def is_date_newer(self, new_date: str, current_date: str) -> bool:
        new_mod_date = parser.parse(new_date)
        current_mod_date = parser.parse(current_date)
        return new_mod_date > current_mod_date
    
    def create_project(self, **kwargs) -> None:
        """Creates a new project and updates metadata; checks modpack compatibility."""
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

                self.metadata = data["metadata"]
                del data["metadata"]
                self.modpack = Modpack(**data)

                if not self.modpack.check_compatibility():
                    print("Invalid project loaded.")
                    exit(1)
            self.metadata["loaded"] = True
            self.metadata["saved"] = True
            return True
        return False

    def save_project(self, filename: Optional[str] = DEF_FILENAME) -> bool:
        """Saves the current project state to a file."""
        if filename:
            self.metadata["filename"] = filename
        if not self.metadata["filename"]:
            return False

        project_data = self.modpack.export_json()
        project_data["metadata"] = self.metadata
        with open(self.metadata["filename"], 'w') as file:
            json.dump(project_data, file, indent=4)
        self.metadata["saved"] = True
        return True

    async def search_mods(self, **kwargs) -> dict:
        """Searches for mods using the ProjectAPI."""
        result = await self.api.search_project(**kwargs)
        return result
    
    async def add_mod(self, name: str, version: dict, project_info: dict, index: int = 0) -> bool:
        """Adds a mod to the modpack with the given name and version information."""
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

    async def rm_mod(self, index: int) -> bool:
        """Removes a mod from the modpack by index."""
        try:
            del self.modpack.mod_data[index]
            self.metadata["saved"] = False
            return True
        except IndexError:
            return False

    
    
    async def update_mod(self, latest_version: list[dict], project_info: dict, index: int) -> bool:
        """Updates selected mods if newer versions are available."""
        name = self.modpack.mod_data[index].project_id
        await self.rm_mod(index)
        await self.add_mod(name, latest_version[0], project_info, index)
    
    def list_projects(self) -> list[str]:
        """Lists all valid projects with their filenames and descriptions."""
        valid_projects = []
        for filename in std.get_project_files():
            try:
                with open(filename, 'r') as file:
                    data = json.load(file)
                    if std.is_valid_project_id(data["metadata"]["project_id"]):
                        valid_projects.append(f'{filename}: {data["title"]}, {data["description"]}')
            except json.JSONDecodeError:
                continue
        return valid_projects
    
    def list_mods(self) -> list[str]:
        """Lists all mods in the loaded project with their names and descriptions."""
        if self.metadata["loaded"]:
            return [f'{m}:\n\t{d}' for m, d in zip(self.modpack.get_mod_list_names(), self.modpack.get_mod_list_descriptions())]
        return None
    
    async def fetch_mods_by_ids(self, ids: list[str]) -> list[dict]:
        """Fetches mods by their IDs concurrently and returns detailed information."""
        mods_ver_info: dict[list] = {"project_info": [], "versions": []}
        
        # Create tasks to fetch versions and project info concurrently
        tasks = [self.api.list_versions(id=id, loaders=[self.modpack.mod_loader], game_versions=[self.modpack.mc_version]) for id in ids]
        tasks.append(self.api.get_projects(ids=ids))

        # Await all tasks to complete
        results = await asyncio.gather(*tasks)

        # Separate the results into versions and project info
        versions_all = results[:len(ids)]
        project_info_all = results[len(ids):]

        # Combine results into the mods_ver_info list
        for versions, project_info in zip(versions_all, project_info_all[0]):
            if versions and project_info:
                mods_ver_info["project_info"].append(project_info)
                mods_ver_info["versions"].append(versions)

        return mods_ver_info
    
    async def export_modpack(self, filename):
        pass
