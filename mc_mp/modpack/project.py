from mc_mp.constants import (FORMAT_VERSION, 
                             GAME, MAX_WORKERS, MOD_PATH, 
                             MR_INDEX, PROJECT_DIR, FABRIC_V)
from mc_mp.modpack.mod import Mod
from mc_mp.modpack.project_api import ProjectAPI
import mc_mp.standard as std
import concurrent.futures as cf
from dateutil import parser
import asyncio
import json
import glob
import os
import aiosqlite
from typing import Dict, Any, List


class ProjectDAO:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_file, check_same_thread=False)
        await self.create_tables()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if hasattr(self, 'conn'):
            await self.conn.close()

    async def create_tables(self):
        async with self.conn.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS Project (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uuid TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    mc_version TEXT,
                    mod_loader TEXT,
                    client_side TEXT,
                    server_side TEXT,
                    slug TEXT UNIQUE
                )''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS Mod (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_id INTEGER,
                    project_id TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    name TEXT,
                    changelog TEXT,
                    version_number TEXT,
                    mc_versions TEXT,
                    mod_loaders TEXT,
                    mod_id TEXT,
                    date_published TEXT,
                    dependencies TEXT,
                    files TEXT,
                    FOREIGN KEY(parent_id) REFERENCES Project(id)
                )''')
            await self.conn.commit()

    async def insert_project(self, project_data: Dict[str, Any]) -> int:
        async with self.conn.cursor() as cursor:
            await cursor.execute('''
                INSERT OR REPLACE INTO Project (
                    uuid, title, description, mc_version, 
                    mod_loader, client_side, server_side, slug
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (project_data["uuid"], project_data["title"], project_data["description"], 
                      project_data["mc_version"], project_data["mod_loader"], project_data["client_side"], 
                      project_data["server_side"], project_data["slug"]))
            await self.conn.commit()
            return cursor.lastrowid

    async def insert_mods(self, parent_id: int, mod_data: List[Mod]):
        async with self.conn.cursor() as cursor:
            await cursor.executemany('''
                INSERT INTO Mod (
                    parent_id, project_id, title, description, 
                    name, changelog, version_number, mc_versions, mod_loaders, 
                    mod_id, date_published, dependencies, files)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', [(
                    parent_id, mod.project_id, mod.title, mod.description,
                    mod.name, mod.changelog, mod.version_number, json.dumps(mod.mc_versions), 
                    json.dumps(mod.mod_loaders, ensure_ascii=False), mod.id, mod.date_published,
                    json.dumps(mod.dependencies, ensure_ascii=False), json.dumps(mod.files, ensure_ascii=False)
                ) for mod in mod_data])
            await self.conn.commit()

    async def fetch_project(self, slug: str) -> tuple[List[tuple], List[str]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM Project WHERE slug=?", (slug,))
            columns = [desc[0] for desc in cursor.description]
            project_data = await cursor.fetchone()
            return project_data, columns

    async def fetch_mods(self, parent_id: int) -> tuple[List[tuple], List[str]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM Mod WHERE parent_id=?", (parent_id,))
            columns = [desc[0] for desc in cursor.description]
            mods_data = await cursor.fetchall()
            return mods_data, columns

    async def fetch_project_names(self) -> List[str]:
        
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT slug FROM Project")
            files = await cursor.fetchall()
            return [file[0] for file in files]
    
class Project:
    api: ProjectAPI
    metadata: Dict[str, Any] = {
        "loaded": False,
        "saved": True,
        "slug": "project1",
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
        self.db_file = db_file
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._processing_mods: set = set()
    
    async def create_tables(self) -> None:
        async with ProjectDAO(self.db_file) as dao:
            await dao.create_tables()
            
    @std.sync_timing
    def is_mod_installed(self, id: str) -> int:
        return std.get_index([m.project_id for m in self.mod_data], id)

    @std.sync_timing
    def is_date_newer(self, new_date: str, current_date: str) -> bool:
        new_mod_date = parser.parse(new_date)
        current_mod_date = parser.parse(current_date)
        return new_mod_date > current_mod_date
    
    @std.sync_timing
    def sort_mods(self) -> None:
        self.mod_data.sort(key=lambda mod: mod.project_id)

    @std.sync_timing
    def get_mods_name_ver(self) -> List[str]:
        return [f"{item.title} - {item.version_number}" for item in self.mod_data]

    @std.sync_timing
    def get_mods_descriptions(self) -> List[str]:
        return [item.description for item in self.mod_data]

    async def get_project_files(self) -> list:
        """Returns a sorted list of JSON files in the current directory."""
        async with ProjectDAO(self.db_file) as dao:
            return await dao.fetch_project_names()

    @std.sync_timing
    def create_project(self, **kwargs) -> bool:
        # Create a new modpack project with provided kwargs
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.metadata.update({
                "loaded": True,
                "saved": False,
                "project_id": std.generate_project_id()
            })
            self.mod_data.clear()
            return True
        except Exception as e:
            std.eprint(f"[ERROR] Failed to create project: {e}")
            return False
    
    @std.async_timing
    async def load_project(self, slug: str) -> bool:
        async with ProjectDAO(self.db_file) as dao:
            project_data, project_columns = await dao.fetch_project(slug)
            
            if project_data:
                # Update metadata with project details
                self.metadata.update({
                    "loaded": True,
                    "saved": True,
                    "project_id": project_data[1],
                    "slug": project_data[8]
                })
                for key, value in dict(zip(project_columns, project_data)).items():
                    setattr(self, key, value)

                # Clear existing mods and load new ones
                self.mod_data.clear()
                mods_data, mod_columns = await dao.fetch_mods(project_data[0])
                for mod_row in mods_data:
                    mod_item = dict(zip(mod_columns, mod_row))
                    mod = Mod()
                    mod.load_json(mod_item)
                    self.mod_data.append(mod)

                return True
            return False

    @std.async_timing
    async def save_project(self, slug: str = "") -> bool:
        slug = slug if slug != "" else self.metadata["slug"]
        if not self.metadata["loaded"]:
            std.eprint("[ERROR] Project must be created before saving.")
            return False

        try:
            async with ProjectDAO(self.db_file) as dao:
                parent_id = await dao.insert_project({
                    "uuid": self.metadata["uuid"],
                    "title": self.title,
                    "description": self.description,
                    "mc_version": self.mc_version,
                    "mod_loader": self.mod_loader,
                    "client_side": self.client_side,
                    "server_side": self.server_side,
                    "slug": slug
                })
                await dao.insert_mods(parent_id, self.mod_data)

            self.metadata["saved"] = True
            self.metadata["slug"] = slug
            return True
        except Exception as e:
            std.eprint(f"[ERROR] Failed to save project: {e}")
            return False

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
            title=project_info.get("title", ""),
            description=project_info.get("description", ""),
            name=version.get("name", ""),
            changelog=version.get("changelog", ""),
            version_number=version.get("version_number", ""),
            dependencies=version.get("dependencies", []),
            mc_versions=version.get("game_versions", []),
            mod_loaders=version.get("loaders", []),
            id=version.get("id", ""),
            project_id=version.get("project_id", ""),
            date_published=version.get("date_published", ""),
            files=version.get("files", [])
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
            (version_list[0].get("project_id", "") if version_list else ""): (version_list if version_list else [])
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

        if not std.check_hash(f'{PROJECT_DIR}/{file_info["slug"]}', file_info["hashes"]):
            std.eprint(f"[ERROR] Wrong hash for file: {file_info['slug']}")
            os.remove(f'{PROJECT_DIR}/{file_info["slug"]}')
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
                self.title = new_var
            case std.Setting.DESCRIPTION:
                self.description = new_var
            case std.Setting.MC_VERSION:
                self.mc_version = new_var
            case std.Setting.MOD_LOADER:
                self.mod_loader = new_var
            case std.Setting.BUILD_VERSION:
                self.build_version = new_var
            case std.Setting.CLIENT_SIDE:
                self.client_side = new_var
            case std.Setting.SERVER_SIDE:
                self.server_side = new_var
            case _:
                return False
        
        return True
