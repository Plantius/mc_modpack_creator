import requests
from typing import Optional, Dict, Any
from . import API_BASE, HEADERS

class ProjectAPI:
    """Handles API interactions for project-related data."""

    @staticmethod
    def parse_url(params: Dict[str, Any]) -> str:
        """Converts a dictionary to a URL query string."""
        return '&'.join(f'{key}={value}' for key, value in params.items()).replace('\'', '\"')

    @staticmethod
    def is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]:
        """Checks if the given project name or ID exists on Modrinth."""
        response = requests.get(f"{API_BASE}/project/{slug_or_id}/check", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_dependencies(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves all dependencies of a given project."""
        if ProjectAPI.is_slug_valid(project_name) is None:
            return None
        
        response = requests.get(f"{API_BASE}/project/{project_name}/dependencies", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def search_project(**kwargs) -> Optional[Dict[str, Any]]:
        """Searches for projects using various filters and sorting options."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        response = requests.get(f"{API_BASE}/search", params=ProjectAPI.parse_url(params), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_project(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific project."""
        if ProjectAPI.is_slug_valid(project_name) is None:
            return None

        response = requests.get(f"{API_BASE}/project/{project_name}", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    
    @staticmethod
    def list_versions(project_name: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Lists versions of a given project with optional filtering."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        if ProjectAPI.is_slug_valid(project_name) is None:
            return None

        response = requests.get(f"{API_BASE}/project/{project_name}/version", params=ProjectAPI.parse_url(params), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    
    @staticmethod
    def get_version(version_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific version by ID."""
        response = requests.get(f"{API_BASE}/version/{version_id}", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    
    @staticmethod
    def get_versions(ids: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about multiple versions by their IDs."""
        params = {'ids': ids}
        response = requests.get(f"{API_BASE}/versions", params=ProjectAPI.parse_url(params), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
