from mc_mp.constants import (DEF_FILENAME, FORMAT_VERSION, 
                             GAME, MAX_WORKERS, MOD_PATH, 
                             MR_INDEX, PROJECT_DIR, FABRIC_V, DEF_EXT)
from mc_mp.modpack.mod import Mod
from mc_mp.modpack.project_api import ProjectAPI
import mc_mp.standard as std
import concurrent.futures as cf
from dateutil import parser
import asyncio
import json
import glob
import os
import sqlite3
from typing import Optional, Dict, Any, List

class Project:
    conn: sqlite3.Connection
    api: ProjectAPI
    metadata: Dict[str, Any] = {
        "loaded": False,
        "saved": True,
        "filename": "project1",
        "uuid": None
    }
    title: str = "Modpack"
    description: str = "A modpack"
    build_date: str = "2024-01-01"
    build_version: str = "0.1"
    mc_version: str = "1.19"
    mod_loader: str = "fabric"
    client_side: str = "required"
    server_side: str = "optional"
    mod_data: list[Mod] = []

    def __init__(self, db_file: str = "project1.db", **kwargs) -> None:
        # Initialize database and create tables
        self.api = ProjectAPI()
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._processing_mods: set = set()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Create Project table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            title TEXT,
            description TEXT,
            mc_version TEXT,
            mod_loader TEXT,
            client_side TEXT,
            server_side TEXT,
            filename TEXT UNIQUE
        )''')

        # Create Mod table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Mod (
            parent_id INTEGER,
            project_id TEXT,
            title TEXT,
            description TEXT,
            name TEXT,
            version_number TEXT,
            mc_versions TEXT,
            mod_loaders TEXT,
            date_published TEXT,
            dependencies TEXT,
            files TEXT,
            PRIMARY KEY (parent_id, project_id),
            FOREIGN KEY(parent_id) REFERENCES Project(id)
        )''')
        self.conn.commit()

    @std.sync_timing
    def is_mod_installed(self, id: str) -> int:
        return std.get_index([m.project_id for m in self.mod_data], id)

    @std.sync_timing
    def is_date_newer(self, new_date: str, current_date: str) -> bool:
        new_mod_date = parser.parse(new_date)
        current_mod_date = parser.parse(current_date)
        return new_mod_date > current_mod_date

    @std.sync_timing
    def create_project(self, **kwargs) -> None:
        # Create a new modpack project with provided kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.metadata.update({
            "loaded": True,
            "saved": False,
            "project_id": std.generate_project_id()
        })

    @std.async_timing
    async def load_project(self, filename: str) -> bool:
        cursor = self.conn.cursor()
        # Load project metadata from database
        cursor.execute("SELECT * FROM Project WHERE filename=?", (filename,))
        project_data = cursor.fetchone()

        if project_data:
            self.metadata.update({
                "loaded": True,
                "saved": True,
                "project_id": project_data[1],
                "filename": project_data[8]
            })
            for key, value in  {"title": project_data[2],
                                "description": project_data[3],
                                "mc_version": project_data[4],
                                "mod_loader": project_data[5],
                                "client_side": project_data[6],
                                "server_side": project_data[7]}.items():
                setattr(self, key, value)
                

            # Load mods associated with the project
            cursor.execute("SELECT * FROM Mod WHERE parent_id=?", (project_data[0],))
            mods_data = cursor.fetchall()
            mods_data = [[item for item in mod] for mod in mods_data]
            for i in []:
                print(dict(i))
            self.mod_data = [Mod(**dict(zip([c[0] for c in cursor.description][1:], mod[1:]))) for mod in mods_data]

            return True
        return False

    @std.async_timing
    async def save_project(self, filename: str="") -> bool:
        filename = filename if filename != "" else self.metadata["filename"]
        cursor = self.conn.cursor()

        # Save project metadata
        cursor.execute('''
        INSERT OR REPLACE INTO Project (
            uuid, title, description, mc_version, 
            mod_loader, client_side, server_side, filename
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.metadata["uuid"], self.title, self.description, 
              self.mc_version, self.mod_loader, self.client_side, 
              self.server_side, filename))

        parent_id = cursor.lastrowid

        # Save associated mods
        for mod in self.mod_data:
            cursor.execute('''
            INSERT INTO Mod (
                parent_id, project_id, title, description, 
                name, version_number, mc_versions, mod_loaders, 
                date_published, dependencies, files)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                parent_id, mod.project_id, mod.title, mod.description,
                mod.name, mod.version_number, json.dumps(mod.mc_versions), 
                json.dumps(mod.mod_loaders), mod.date_published,
                json.dumps(mod.dependencies), json.dumps(mod.files)
            ))

        self.conn.commit()
        self.metadata["saved"] = True
        return True

    @std.async_timing
    async def search_mods(self, **kwargs) -> dict:
        result = await self.api.search_project(**kwargs)
        return result

    @std.sync_timing
    def add_mod(self, name: str, version: dict, project_info: dict, index: int = 0) -> bool:
        if not any([project_info, version]):
            std.eprint(f"[ERROR] Could not find mod with name: {name}")
            return False

        self.mod_data.insert(index, Mod(
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
        self.sort_mods()
        return True

    @std.sync_timing
    def rm_mod(self, index: int) -> bool:
        try:
            del self.mod_data[index]
            self.metadata["saved"] = False
            self.sort_mods()
            return True
        except IndexError:
            return False

    @std.sync_timing
    def update_mod(self, latest_version: dict, project_info: dict, index: int) -> bool:
        self.mod_data[index].update_self(latest_version, project_info)
        self.sort_mods()
        self.metadata["saved"] = False
        return True

    @std.sync_timing
    def update_mods(self, latest_versions, project_infos, indices) -> bool:
        for index, latest_version, project_info in zip(indices, latest_versions, project_infos):
            self.mod_data[index].update_self(latest_version, project_info)
        self.sort_mods()
        self.metadata["saved"] = False
        return True

    @std.sync_timing
    def list_mods(self) -> list[str]:
        if self.metadata["loaded"]:
            return [f'{m}:\n\t{d}' for m, d in zip(self.get_mods_name_ver(), self.get_mods_descriptions())]
        return []

    @std.sync_timing
    def get_versions_id(self, id: str, loop) -> list[dict]:
        future = asyncio.run_coroutine_threadsafe(self.api.list_versions(id=id, loaders=[self.mod_loader], game_versions=[self.mc_version]), loop)
        return future.result()

    @std.sync_timing
    def get_project_info_ids(self, ids: list[str], loop) -> list[dict]:
        future = asyncio.run_coroutine_threadsafe(self.api.get_projects(ids=ids), loop)
        return future.result()

    @std.async_timing
    async def fetch_mods_by_ids(self, ids: list[str]) -> list[dict]:
        mods_ver_info: list = []
        loop = asyncio.get_running_loop()

        with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            tasks_vers = [loop.run_in_executor(executor, self.get_versions_id, id, loop) for id in ids]
            tasks_info = loop.run_in_executor(executor, self.get_project_info_ids, ids, loop)
            res_ver = await asyncio.gather(*tasks_vers)
            res_info = await asyncio.gather(tasks_info)

        version_map: dict = {
            version_list[0].get("project_id", ""): (version_list if version_list else [])
            for version_list in res_ver
        }
        mods_ver_info = [
            {**project_info, "versions": version_map.get(project_info.get("id"), [])}
            for project_info in res_info[0]
            if project_info.get("id") in version_map
        ]
        return mods_ver_info

    @std.sync_timing
    def download_file(self, file_info, loop) -> bool:
        future = asyncio.run_coroutine_threadsafe(self.api.get_file_from_url(**file_info), loop)
        future.result()

        if not std.check_hash(f'{PROJECT_DIR}/{file_info["filename"]}', file_info["hashes"]):
            std.eprint(f"[ERROR] Wrong hash for file: {file_info['filename']}")
            os.remove(f'{PROJECT_DIR}/{file_info["filename"]}')
            return False
        return True

    @std.async_timing
    async def download_mods(self, dir_name: str) -> bool:
        try:
            os.makedirs(dir_name)
        except FileExistsError:
            std.eprint("[ERROR] Directory already exists")
            return False

        # Prepare file information
        files = [file[0] for file in [[file for file in m.files if file["primary"]] for m in self.mod_data]]

        loop = asyncio.get_running_loop()
        with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            tasks = [
                loop.run_in_executor(executor, self.download_file, file, loop)
                for file in files
            ]
            results = await asyncio.gather(*tasks)

        # Handle errors
        if not any(results):
            std.eprint("[ERROR] One or more files failed to download or check correctly.")
            return False
        return True

    @std.sync_timing
    def convert_file_to_mp_format(self, mod: dict) -> dict:
        return {
            "path": f"{MOD_PATH}{mod['filename']}",
            "hashes": mod['hashes'],
            "env": mod["env"],
            "downloads": [mod["url"]],
            "fileSize": mod["size"]
        }

    @std.sync_timing
    def sort_mods(self) -> None:
        self.mod_data.sort(key=lambda mod: mod.project_id)

    @std.sync_timing
    def get_mods_name_ver(self) -> List[str]:
        return [f"{item.title} - {item.version_number}" for item in self.mod_data]

    @std.sync_timing
    def get_mods_descriptions(self) -> List[str]:
        return [item.description for item in self.mod_data]

    def get_project_files(self) -> list:
        """Returns a sorted list of JSON files in the current directory."""
        cursor = self.conn.cursor()
        # Load project metadata from database
        files = [file[0] for file in cursor.execute("SELECT filename FROM Project")]
        return files if files else []

    @std.async_timing
    async def export_modpack(self, filename: str) -> bool:
        try:
            os.makedirs(PROJECT_DIR)
        except FileExistsError:
            pass

        modpack_json: dict = {
            "formatVersion": FORMAT_VERSION, 
            "game": GAME,
            "versionId": self.mc_version,
            "name": self.title,
            "summary": self.description,
            "files": [],
            "dependencies": {
                "minecraft": self.mc_version,
                self.mod_loader: FABRIC_V
            }
        }

        for mod in self.mod_data:
            for mod_file in mod.files:
                if not mod_file["primary"]:
                    continue
                mod_file["env"] = {
                    "client": self.client_side,
                    "server": self.server_side
                }
                modpack_json["files"].append(self.convert_file_to_mp_format(mod_file))

        with open(f"{PROJECT_DIR}/{MR_INDEX}", 'w', encoding='utf8') as index_file:
            json.dump(modpack_json, index_file, indent=3, ensure_ascii=False)

        try:
            std.zip_dir(filename, PROJECT_DIR)
            files = glob.glob(f'{PROJECT_DIR}/*')
            for file in files:
                os.remove(file)
            os.rmdir(PROJECT_DIR)
        except Exception as e:
            std.eprint(f"[ERROR] Could not create archive: {e}")
            return False

        print("[INFO] Modpack exported successfully.")
        return True
       
    @std.sync_timing
    def update_settings(self, new_var: str, index: std.Setting) -> bool:
        """
        Updates project settings based on the provided index.

        Args:
            new_var (str): The new value to set for the specified setting.
            index (std.Setting): The setting to update.

        Returns:
            bool: True if the setting is updated successfully, otherwise False.
        """
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
