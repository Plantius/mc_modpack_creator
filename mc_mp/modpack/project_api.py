import aiohttp
from typing import Optional, Dict, Any
from . import API_BASE, HEADERS

class ProjectAPI:
    """Handles API interactions for project-related data."""

    @staticmethod
    async def request(endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Handles GET requests and returns JSON response."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE}{endpoint}", params=params, headers=HEADERS) as response:
                response.raise_for_status()
                return await response.json()
            
    @staticmethod
    def parse_url(params: Dict[str, Any]) -> str:
        """Converts a dictionary to a URL query string."""
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
        """Retrieves all dependencies of a given project."""
        if await ProjectAPI.is_slug_valid(project_name) is None:
            return None
        try:
            return await ProjectAPI.request(f"/project/{project_name}/dependencies")
        except:
            return None
        
        
    @staticmethod
    async def search_project(**kwargs) -> Optional[Dict[str, Any]]:
        """Searches for projects using various filters and sorting options."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request(f"/search", params=ProjectAPI.parse_url(params))
        except:
            return None
        
    @staticmethod
    async def get_project(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific project."""
        if await ProjectAPI.is_slug_valid(project_name) is None:
            return None
        return await ProjectAPI.request(f"/project/{project_name}")
    
    @staticmethod
    async def get_projects(**kwargs) -> Optional[Dict[str, Any]]:
        """Retrieves information about a list of projects."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        if any([await ProjectAPI.is_slug_valid(project_name) for project_name in params["ids"]]):
            return None
        return await ProjectAPI.request(f"/projects", params=params)

    @staticmethod
    async def list_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """Lists versions of a given project with optional filtering."""
        params = {k: v for k, v in kwargs.items() if v is not None and k != "id"}
        try:
            return await ProjectAPI.request(f"/project/{kwargs['id']}/version", params=ProjectAPI.parse_url(params))
        except:
            return None
    
    @staticmethod
    async def get_version(version_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific version by ID."""
        try:
            return await ProjectAPI.request(f"/version/{version_id}")
        except:
            return None
    @staticmethod
    async def get_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """Retrieves information about multiple versions by their IDs."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request(f"/versions", params=params)
        except:
            return None
