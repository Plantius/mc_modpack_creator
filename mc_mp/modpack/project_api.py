"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/project_api.py
Last Edited: 2024-09-07

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from aiohttp import ClientSession
from typing import Optional, Dict, Any

from constants import API_BASE, HEADERS
from constants import PROJECT_DIR

class ProjectAPI:
    """Handles interactions with the Modrinth API for project-related data."""

    @staticmethod
    async def request(endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Makes a GET request to the specified API endpoint and returns the JSON response."""
        async with ClientSession() as session:
            async with session.get(f"{API_BASE}{endpoint}", params=params, headers=HEADERS) as response:
                response.raise_for_status()
                return await response.json()
            
    @staticmethod
    def parse_url(params: Dict[str, Any]) -> str:
        """Converts a dictionary of parameters into a URL query string."""
        return '&'.join(f'{key}={value}' for key, value in params.items()).replace('\'', '\"').replace(" ", "")

    @staticmethod
    async def is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]:
        """Checks if the given project name or ID exists on Modrinth."""
        try:
            return await ProjectAPI.request(f"/project/{slug_or_id}/check")
        except:
            return None
        
    @staticmethod
    async def get_dependencies(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves all dependencies for the specified project."""
        try:
            return await ProjectAPI.request(f"/project/{project_name}/dependencies")
        except:
            return None
        
    @staticmethod
    async def search_project(**kwargs) -> Optional[Dict[str, Any]]:
        """Searches for projects with various filters and sorting options."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request(f"/search", params=ProjectAPI.parse_url(params))
        except:
            return None
        
    @staticmethod
    async def get_project(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves detailed information about a specific project."""
        try: 
            return await ProjectAPI.request(f"/project/{project_name}")
        except:
            print(f"[ERROR] Could not get project {project_name}")
            return None
        
    @staticmethod
    async def get_projects(**kwargs) -> Optional[Dict[str, Any]]:
        """Retrieves information about multiple projects."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        return await ProjectAPI.request(f"/projects", params=ProjectAPI.parse_url(params))

    @staticmethod
    async def list_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """Lists versions of a specified project with optional filtering."""
        params = {k: v for k, v in kwargs.items() if v is not None and k != "id"}
        try:
            return await ProjectAPI.request(f"/project/{kwargs['id']}/version", params=ProjectAPI.parse_url(params))
        except:
            return None
    
    @staticmethod
    async def get_version(version_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves detailed information about a specific version by its ID."""
        try:
            return await ProjectAPI.request(f"/version/{version_id}")
        except:
            print(f"[ERROR] Could not retreive versions of {version_id}")
            return None
    
    @staticmethod
    async def get_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """Retrieves information about multiple versions by their IDs."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request(f"/versions", params=params)
        except:
            return None
    
    @staticmethod
    async def get_file_from_url(**kwargs) -> None:
        """Retrieves information about multiple versions by their IDs."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        async with ClientSession() as session:
            async with session.get(params["url"]) as response:
                if response.status == 200:
                    data = await response.read()
                    with open(f'{PROJECT_DIR}/{params["filename"]}', "wb") as file:
                        file.write(data)