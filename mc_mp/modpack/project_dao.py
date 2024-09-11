"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/project_dao.py
Last Edited: 2024-09-10

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from typing import Dict, Any, List
import aiosqlite
from mc_mp.modpack.mod import Mod
import mc_mp.standard as std

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
            # Project table
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

            # Mod table
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
                    mod_id TEXT,
                    date_published TEXT,
                    FOREIGN KEY(parent_id) REFERENCES Project(id) ON DELETE CASCADE
                )''')

            # Separate tables for lists (mod_versions, mod_loaders, dependencies, files)
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS ModVersion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mod_id INTEGER,
                    mc_version TEXT,
                    FOREIGN KEY(mod_id) REFERENCES Mod(id) ON DELETE CASCADE
                )''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS ModLoader (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mod_id INTEGER,
                    loader TEXT,
                    FOREIGN KEY(mod_id) REFERENCES Mod(id) ON DELETE CASCADE
                )''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS ModDependency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mod_id INTEGER,
                    version_id TEXT,
                    project_id TEXT,
                    file_name TEXT,
                    dependency_type TEXT,
                    FOREIGN KEY(mod_id) REFERENCES Mod(id) ON DELETE CASCADE
                )''')

            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS ModFile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mod_id INTEGER,
                    filename TEXT,
                    size INTEGER,
                    url TEXT,
                    sha512 TEXT,
                    sha1 TEXT,
                    primary_flag BOOLEAN,
                    file_type TEXT,
                    FOREIGN KEY(mod_id) REFERENCES Mod(id) ON DELETE CASCADE
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

    async def remove_project(self, slug: str) -> bool:
        """
        Remove a project and all associated mods, versions, loaders, dependencies, and files
        based on the project slug.
        """
        async with self.conn.cursor() as cursor:
            # First, fetch the project by slug to ensure it exists
            await cursor.execute("SELECT id FROM Project WHERE slug=?", (slug,))
            project = await cursor.fetchone()
            
            if not project:
                # If no project exists with the given slug, return False
                std.eprint(f"[ERROR] No project found with slug: {slug}")
                return False
            
            # Now delete the project
            await cursor.execute("DELETE FROM Project WHERE slug=?", (slug,))
            await self.conn.commit()
            return True
    
    async def insert_mod(self, parent_id: int, mod: Mod):
        async with self.conn.cursor() as cursor:
            # Insert mod data into the Mod table
            await cursor.execute('''
                INSERT OR REPLACE INTO Mod (
                    parent_id, project_id, title, description, 
                    name, changelog, version_number, mod_id, date_published
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                parent_id, mod.project_id, mod.title, mod.description, mod.name,
                mod.changelog, mod.version_number, mod.mod_id, mod.date_published
            ))
            mod_id = cursor.lastrowid  # Get the inserted mod ID

            # Insert Minecraft versions (mc_versions)
            await cursor.executemany('''
                INSERT OR REPLACE INTO ModVersion (mod_id, mc_version) VALUES (?, ?)
            ''', [(mod_id, version) for version in mod.mc_versions])

            # Insert loaders (mod_loaders)
            await cursor.executemany('''
                INSERT OR REPLACE INTO ModLoader (mod_id, loader) VALUES (?, ?)
            ''', [(mod_id, loader) for loader in mod.mod_loaders])

            # Insert dependencies (dependencies)
            await cursor.executemany('''
                INSERT OR REPLACE INTO ModDependency (mod_id, version_id, project_id, file_name, dependency_type) VALUES (?, ?, ?, ?, ?)
            ''', [(mod_id, dep["version_id"], dep["project_id"], dep["file_name"], dep["dependency_type"]) for dep in mod.dependencies])

            # Insert files (files)
            await cursor.executemany('''
                INSERT OR REPLACE INTO ModFile (mod_id, filename, size, url, sha512, sha1, primary_flag, file_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', [
                (mod_id, file["filename"], file["size"], file["url"], file["hashes"]["sha512"], file["hashes"]["sha1"], file["primary"], file["file_type"])
                for file in mod.files
            ])
 
            await self.conn.commit()

    async def remove_mods_not_in_list(self, parent_id: int, mod_data: List[Mod]):
        """
        Delete mods from the database that are not present in the given mod_data list.
        """
        async with self.conn.cursor() as cursor:
            # Get the current mods in the database for the project
            await cursor.execute("SELECT mod_id FROM Mod WHERE parent_id=?", (parent_id,))
            existing_mod_ids = {row[0] for row in await cursor.fetchall()}  # Set of mod_ids from the DB

            # Get the mod_ids from the provided mod_data list
            current_mod_ids = {mod.mod_id for mod in mod_data}

            # Mods to delete: present in DB but not in the current mod_data list
            mods_to_delete = existing_mod_ids - current_mod_ids

            # Delete the mods from the database that are not in the current mod_data list
            if mods_to_delete:
                await cursor.executemany("DELETE FROM Mod WHERE mod_id=?", [(mod_id,) for mod_id in mods_to_delete])
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
    
    async def fetch_mods_dependencies(self, mod_id: int) -> tuple[List[tuple], List[str]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM ModDependency WHERE mod_id=?", (mod_id,))
            columns = [desc[0] for desc in cursor.description]
            mods_data = await cursor.fetchall()
            return mods_data, columns
    
    async def fetch_mods_loaders(self, mod_id: int) -> tuple[List[tuple], List[str]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM ModLoader WHERE mod_id=?", (mod_id,))
            columns = [desc[0] for desc in cursor.description]
            mods_data = await cursor.fetchall()
            return mods_data, columns
    
    async def fetch_mods_versions(self, mod_id: int) -> tuple[List[tuple], List[str]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM ModVersion WHERE mod_id=?", (mod_id,))
            columns = [desc[0] for desc in cursor.description]
            mods_data = await cursor.fetchall()
            return mods_data, columns
    
    async def fetch_mods_files(self, mod_id: int) -> tuple[List[tuple], List[str]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM ModFile WHERE mod_id=?", (mod_id,))
            columns = [desc[0] for desc in cursor.description]
            mods_data = await cursor.fetchall()
            return mods_data, columns

    async def fetch_project_names(self) -> List[str]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT slug FROM Project")
            files = await cursor.fetchall()
            return [file[0] for file in files]
