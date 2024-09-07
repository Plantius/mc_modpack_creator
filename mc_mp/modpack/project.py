"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/project.py
Last Edited: 2024-09-07

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
import numpy as np
from mc_mp.constants import DEF_FILENAME, FORMAT_VERSION, GAME, MAX_WORKERS, MOD_PATH, MR_INDEX, MRPACK, PROJECT_DIR, FABRIC_V, DEF_EXT
from mc_mp.modpack.modpack import Modpack
from mc_mp.modpack.mod import Mod
from mc_mp.modpack.project_api import ProjectAPI
import mc_mp.standard as std
import concurrent.futures as cf
from typing import Optional, Dict, Any
from dateutil import parser
import asyncio
import functools
import json
import glob
import os

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
        """
        Checks if a mod is installed by ID and returns its index.

        Args:
            id (str): The mod ID to check.

        Returns:
            int: The index of the mod in the mod_data, or -1 if not found.
        """
        return std.get_index([m.project_id for m in self.modpack.mod_data], id)

    def is_date_newer(self, new_date: str, current_date: str) -> bool:
        """
        Compares two date strings to check if new_date is more recent than current_date.

        Args:
            new_date (str): The newer mod date.
            current_date (str): The current mod date.

        Returns:
            bool: True if new_date is later than current_date, otherwise False.
        """
        new_mod_date = parser.parse(new_date)
        current_mod_date = parser.parse(current_date)
        return new_mod_date > current_mod_date

    def create_project(self, **kwargs) -> None:
        """
        Creates a new project with modpack and updates metadata.

        Raises an error if the modpack is not compatible.
        """
        self.modpack = Modpack(**kwargs)
        self.metadata.update({
            "loaded": True,
            "saved": False,
            "project_id": std.generate_project_id()
        })
        if not self.modpack.check_compatibility():
            std.eprint("[ERROR]: Invalid project created.")
            exit(1)

    @std.async_timing
    async def load_project(self, filename: str) -> bool:
        """
        Loads project data from a file and initializes the modpack.

        Args:
            filename (str): The file name to load the project from.

        Returns:
            bool: True if the file is loaded successfully, otherwise False.
        """
        if not os.path.exists(filename):
            return False
        loop = asyncio.get_running_loop()
        with open(filename, 'r') as file:
            data = await loop.run_in_executor(None, json.load, file)
        
        if not std.is_valid_project_id(data["metadata"]["project_id"]):
            std.eprint("[ERROR] Invalid project file.")
            exit(1)

        self.metadata = data["metadata"]
        del data["metadata"]
        self.modpack = Modpack(**data)
        
        self.metadata["loaded"] = True
        self.metadata["saved"] = True
        self.modpack.sort_mods()
        return True

    async def save_project(self, filename: Optional[str] = DEF_FILENAME) -> bool:
        """
        Saves the current project state to a file.

        Args:
            filename (Optional[str]): The file name to save the project to.

        Returns:
            bool: True if the project is saved successfully, otherwise False.
        """
        if filename:
            self.metadata["filename"] = filename
        if not self.metadata["filename"]:
            return False

        project_data = self.modpack.export_json()
        project_data["metadata"] = self.metadata
        
        loop = asyncio.get_running_loop()
        with open(f'{self.metadata["filename"]}.{DEF_EXT}', 'w') as file:
            await loop.run_in_executor(None, functools.partial(json.dump, project_data, file, indent=4))
        
        self.metadata["saved"] = True
        return True

    @std.async_timing
    async def search_mods(self, **kwargs) -> dict:
        """
        Searches for mods using the ProjectAPI.

        Args:
            **kwargs: Filter and search parameters for the mod search.

        Returns:
            dict: The search results from the API.
        """
        result = await self.api.search_project(**kwargs)
        return result

    def add_mod(self, name: str, version: dict, project_info: dict, index: int = 0) -> bool:
        """
        Adds a mod to the modpack.

        Args:
            name (str): The mod name.
            version (dict): Version information.
            project_info (dict): The project information.
            index (int): The index to insert the mod at.

        Returns:
            bool: True if the mod is added successfully, otherwise False.
        """
        if not any([project_info, version]):
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
        self.modpack.sort_mods()
        return True

    def rm_mod(self, index: int) -> bool:
        """
        Removes a mod from the modpack by index.

        Args:
            index (int): The index of the mod to remove.

        Returns:
            bool: True if the mod is removed successfully, otherwise False.
        """
        try:
            del self.modpack.mod_data[index]
            self.metadata["saved"] = False
            self.modpack.sort_mods()
            return True
        except IndexError:
            return False

    def update_mod(self, latest_version: dict, project_info: dict, index: int) -> bool:
        """
        Updates selected mods if newer versions are available.

        Args:
            latest_version (dict): The latest version information.
            project_info (dict): The project information.
            index (int): The index of the mod to update.

        Returns:
            bool: True if the mod is updated successfully, otherwise False.
        """
        self.modpack.mod_data[index].update_self(latest_version, project_info)
        self.modpack.sort_mods()
        self.metadata["saved"] = False
        return True

    def update_mods(self, latest_versions, project_infos, indices) -> bool:
        """
        Updates multiple mods based on new version and project information.

        Args:
            latest_versions (list[dict]): List of latest version information.
            project_infos (list[dict]): List of project information.
            indices (list[int]): List of indices of mods to update.

        Returns:
            bool: True if mods are updated successfully, otherwise False.
        """
        for index, latest_version, project_info in zip(indices, latest_versions, project_infos):
            self.modpack.mod_data[index].update_self(latest_version, project_info)
        self.modpack.sort_mods()
        self.metadata["saved"] = False
        return True

    def list_mods(self) -> list[str]:
        """
        Lists all mods in the loaded project with their names and descriptions.

        Returns:
            list[str]: A list of strings, each containing a mod's name and description.
        """
        if self.metadata["loaded"]:
            return [f'{m}:\n\t{d}' for m, d in zip(self.modpack.get_mods_name_ver(), self.modpack.get_mods_descriptions())]
        return None

    def get_versions_id(self, id: str, loop) -> list[dict]:
        """
        Fetches version information for a specific mod ID.

        Args:
            id (str): The mod ID.
            loop (asyncio.AbstractEventLoop): The event loop to run the async task.

        Returns:
            list[dict]: A list of version information for the mod.
        """
        future = asyncio.run_coroutine_threadsafe(self.api.list_versions(id=id, loaders=[self.modpack.mod_loader], game_versions=[self.modpack.mc_version]), loop)
        return future.result()

    def get_project_info_ids(self, ids: list[str], loop) -> list[dict]:
        """
        Fetches project information for a list of project IDs.

        Args:
            ids (list[str]): List of project IDs.
            loop (asyncio.AbstractEventLoop): The event loop to run the async task.

        Returns:
            list[dict]: A list of project information.
        """
        future = asyncio.run_coroutine_threadsafe(self.api.get_projects(ids=ids), loop)
        return future.result()

    @std.async_timing
    async def fetch_mods_by_ids(self, ids: list[str]) -> list[dict]:
        """
        Fetches mods by their IDs concurrently and returns detailed information.

        Args:
            ids (list[str]): A list of mod IDs.

        Returns:
            list[dict]: A list of mod details, including version information.
        """
        mods_ver_info: list = []
        loop = asyncio.get_running_loop()
        
        with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            tasks_vers = [loop.run_in_executor(executor, self.get_versions_id, id, loop) for id in ids]
            tasks_info = loop.run_in_executor(executor, self.get_project_info_ids, ids, loop)
            res_ver = await asyncio.gather(*tasks_vers)
            res_info = await asyncio.gather(tasks_info)
        
        version_map = {}
        for version_list in res_ver:
            if version_list:
                version = version_list[0]
                project_id = version.get("project_id")
                if project_id:
                    if project_id not in version_map:
                        version_map[project_id] = []
                    version_map[project_id].append(version)
        
        mods_ver_info = []
        for project_info in res_info[0]:
            project_id = project_info.get("id")
            if project_id and project_id in version_map:
                version = version_map[project_id]
                project_info["versions"] = version
                mods_ver_info.append(project_info)
        
        return mods_ver_info

    @std.sync_timing
    def download_file(self, file_info, loop) -> bool:
        """
        Downloads a file and checks its hash.

        Args:
            file_info (dict): The file metadata, including URL and filename.
            loop (asyncio.AbstractEventLoop): The event loop to run the async task.

        Returns:
            bool: True if the file is downloaded and verified successfully, otherwise False.
        """
        future = asyncio.run_coroutine_threadsafe(self.api.get_file_from_url(**file_info), loop)
        future.result()

        if not std.check_hash(f'{PROJECT_DIR}/{file_info["filename"]}', file_info["hashes"]):
            std.eprint(f"[ERROR] Wrong hash for file: {file_info['filename']}")
            os.remove(f'{PROJECT_DIR}/{file_info["filename"]}')
            return False
        return True

    
    def convert_file_to_mp_format(self, mod: dict) -> dict:
        """
        Converts a mod file to the modpack format.

        Args:
            mod (dict): The mod information.

        Returns:
            dict: A dictionary representing the mod file in modpack format.
        """
        return {
            "path": f"{MOD_PATH}{mod['filename']}",
            "hashes": mod['hashes'],
            "env": mod["env"],
            "downloads": [mod["url"]],
            "fileSize": mod["size"]
        }
    
    @std.async_timing
    async def export_modpack(self, filename: str):
        try:
            os.makedirs(PROJECT_DIR)
        except FileExistsError:
            pass
        
        modpack_json = {"formatVersion": FORMAT_VERSION, 
                        "game": GAME,
                        "versionId": self.modpack.mc_version,
                        "name": self.modpack.title,
                        "summary": self.modpack.description,
                        "files": [],
                        "dependencies": {
                            "minecraft": self.modpack.mc_version, 
                            self.modpack.mod_loader if ("fabric" or "quilt") not in self.modpack.mod_loader else f"{self.modpack.mod_loader}-loader" : FABRIC_V}
                        }

        for mod in self.modpack.mod_data:
            for mod_file in mod.files:
                if not mod_file["primary"]:
                    continue
                mod_file["env"] = {"client": self.modpack.client_side,
                                   "server": self.modpack.server_side} 
                modpack_json["files"].append(self.convert_file_to_mp_format(mod_file))

        with open(f"{PROJECT_DIR}/{MR_INDEX}", 'w', encoding='utf8') as index_file:
            json.dump(modpack_json, index_file, indent=3, ensure_ascii=False)
        
        try:
            std.zip_dir(filename, PROJECT_DIR)
            files = glob.glob(f'{PROJECT_DIR}/*')
            for file in files:
                os.remove(file)
            os.rmdir(PROJECT_DIR)    
        except:
            std.eprint("[ERROR] Could not create archive.")
            return
        print("[INFO] Modpack exported successfully.")
        return True


    def update_settings(self, new_var: str, index: std.Setting) -> bool:
        self.metadata["saved"] = False
        match index:
            case std.Setting.TITLE:
                self.modpack.title = new_var
            case std.Setting.DESCRIPTION:
                self.modpack.description = new_var
            case std.Setting.MC_VERSION:
                self.modpack.mc_version = new_var
            case std.Setting.MOD_LOADER:
                self.modpack.mod_loader = new_var
            case std.Setting.BUILD_VERSION:
                self.modpack.build_version = new_var
            case std.Setting.CLIENT_SIDE:
                self.modpack.client_side = new_var
            case std.Setting.SERVER_SIDE:
                self.modpack.server_side = new_var
            case _:
                return False
        return True
