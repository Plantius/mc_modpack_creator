from typing import Dict, Any, List
import aiosqlite
import json
from mc_mp.modpack.mod import Mod

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
                INSERT OR REPLACE INTO Mod (
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