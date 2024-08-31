from .modpack import Modpack
from .mod import Mod
import standard as std
import json, os
import time
from typing import Optional, Dict, Any
from . import DEF_FILENAME, ACCEPT
from .project_api import ProjectAPI
import concurrent.futures as cf
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
        start_time = time.perf_counter()
        result = std.get_index([m.project_id for m in self.modpack.mod_data], id)
        end_time = time.perf_counter()
        print(f"Time taken for is_mod_installed: {end_time - start_time:.4f} seconds")
        return result
    
    def create_project(self, **kwargs) -> None:
        """Creates a new project and updates metadata. Checks modpack compatibility."""
        start_time = time.perf_counter()
        self.modpack = Modpack(**kwargs)
        self.metadata.update({
            "loaded": True,
            "saved": False,
            "project_id": std.generate_project_id()
        })
        if not self.modpack.check_compatibility():
            std.eprint("[ERROR]: Invalid project created.")
            exit(1)
        end_time = time.perf_counter()
        print(f"Time taken for create_project: {end_time - start_time:.4f} seconds")

    def load_project(self, filename: str) -> bool:
        """Loads project data from a file and initializes the modpack."""
        start_time = time.perf_counter()
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
            end_time = time.perf_counter()
            print(f"Time taken for load_project: {end_time - start_time:.4f} seconds")
            return True
        end_time = time.perf_counter()
        print(f"Time taken for load_project (file not found): {end_time - start_time:.4f} seconds")
        return False

    def save_project(self, filename: Optional[str] = DEF_FILENAME) -> bool:
        """Saves the current project state to a file. Uses a default filename if none is provided."""
        start_time = time.perf_counter()
        if filename:
            self.metadata["filename"] = filename
        if not self.metadata["filename"]:
            end_time = time.perf_counter()
            print(f"Time taken for save_project (filename not set): {end_time - start_time:.4f} seconds")
            return False

        project_data = self.modpack.export_json()
        project_data["metadata"] = self.metadata
        with open(self.metadata["filename"], 'w') as file:
            json.dump(project_data, file, indent=4)
        self.metadata["saved"] = True
        end_time = time.perf_counter()
        print(f"Time taken for save_project: {end_time - start_time:.4f} seconds")
        return True

    async def search_mods(self, **kwargs) -> dict:
        """Searches for mods using the ProjectAPI."""
        start_time = time.perf_counter()
        result = await self.api.search_project(**kwargs)
        end_time = time.perf_counter()
        print(f"Time taken for search_mods: {end_time - start_time:.4f} seconds")
        return result
    
    async def add_mod(self, name: str, version: dict, project_info: dict, index: int = 0) -> bool:
        """Adds a mod to the modpack with the given name and version information."""
        start_time = time.perf_counter()
        if any([project_info, version]) is None:
            std.eprint(f"[ERROR] Could not find mod with name: {name}")
            end_time = time.perf_counter()
            print(f"Time taken for add_mod (mod not found): {end_time - start_time:.4f} seconds")
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
        end_time = time.perf_counter()
        print(f"Time taken for add_mod: {end_time - start_time:.4f} seconds")
        return True

    async def rm_mod(self, index: int) -> bool:
        """Removes a mod from the modpack by index."""
        start_time = time.perf_counter()
        try:
            del self.modpack.mod_data[index]
            self.metadata["saved"] = False
            end_time = time.perf_counter()
            print(f"Time taken for rm_mod: {end_time - start_time:.4f} seconds")
            return True
        except IndexError:
            end_time = time.perf_counter()
            print(f"Time taken for rm_mod (index error): {end_time - start_time:.4f} seconds")
            return False

    async def update_mod(self, selected_index: list[int]) -> bool:
        """Updates selected mods if newer versions are available."""
        start_time = time.perf_counter()
        ids = [id.project_id for id in self.modpack.mod_data]
        ids = [ids[i] for i in selected_index]
        mods_versions_info_all = await self.fetch_mods_by_ids(ids)
        
        if not any(mods_versions_info_all):
            std.eprint("[ERROR] Could not find mods.")
            end_time = time.perf_counter()
            print(f"Time taken for update_mod (mods not found): {end_time - start_time:.4f} seconds")
            return False
        
        versions_all = [v["versions"] for v in mods_versions_info_all]
        project_info_all = [i["project_info"] for i in mods_versions_info_all]
        
        for index, latest_version, project_info in zip(selected_index, versions_all, project_info_all):
            new_mod_date = parser.parse(latest_version[0]["date_published"])
            current_mod_date = parser.parse(self.modpack.mod_data[index].date_published)
            
            if new_mod_date > current_mod_date:
                inp = std.get_input(f"There is a newer version available for {self.modpack.mod_data[index].name}, do you want to upgrade? y/n {self.modpack.mod_data[index].version_number} -> {latest_version[0]['version_number']} ")
                if inp == ACCEPT:
                    name = self.modpack.mod_data[index].project_id
                    await self.rm_mod(index)
                    await self.add_mod(name, latest_version[0], project_info, index)
            print(f"{self.modpack.get_mods_name_ver()[index]} is up to date")
        
        end_time = time.perf_counter()
        print(f"Time taken for update_mod: {end_time - start_time:.4f} seconds")
    
    def list_projects(self) -> list[str]:
        """Lists all valid projects with their filenames and descriptions."""
        start_time = time.perf_counter()
        valid_projects = []
        for filename in std.get_project_files():
            try:
                with open(filename, 'r') as file:
                    data = json.load(file)
                    if std.is_valid_project_id(data["metadata"]["project_id"]):
                        valid_projects.append(f'{filename}: {data["title"]}, {data["description"]}')
            except json.JSONDecodeError:
                continue
        end_time = time.perf_counter()
        print(f"Time taken for list_projects: {end_time - start_time:.4f} seconds")
        return valid_projects
    
    def list_mods(self) -> list[str]:
        """Lists all mods in the loaded project with their names and descriptions."""
        start_time = time.perf_counter()
        if self.metadata["loaded"]:
            result = [f'{m}:\n\t{d}' for m, d in zip(self.modpack.get_mod_list_names(), self.modpack.get_mod_list_descriptions())]
            end_time = time.perf_counter()
            print(f"Time taken for list_mods: {end_time - start_time:.4f} seconds")
            return result
        end_time = time.perf_counter()
        print(f"Time taken for list_mods (project not loaded): {end_time - start_time:.4f} seconds")
        return None
    
    async def fetch_mods_by_ids(self, ids: list[str]) -> list[dict]:
        """Fetches mods by their IDs concurrently and returns detailed information."""
        start_time = time.perf_counter()
        mods_ver_info = []

        # Create tasks to fetch versions and project info concurrently
        tasks = [self.api.list_versions(id=id, loaders=[self.modpack.mod_loader], game_versions=[self.modpack.mc_version]) for id in ids]
        tasks += [self.api.get_projects(ids=ids)]

        # Await all tasks to complete
        results = await asyncio.gather(*tasks)

        # Separate the results into versions and project info
        versions_all = results[:len(ids)]
        project_info_all = results[len(ids):]

        # Combine results into the mods_ver_info list
        for versions, project_info in zip(versions_all, project_info_all):
            if versions and project_info:
                mods_ver_info.append({
                    "project_info": project_info,
                    "versions": versions
                })

        end_time = time.perf_counter()
        print(f"Time taken for fetch_mods_by_ids: {end_time - start_time:.4f} seconds")
        return mods_ver_info
