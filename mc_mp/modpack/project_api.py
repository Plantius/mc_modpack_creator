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
    def request(endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Handles GET requests and returns JSON response."""
        response = requests.get(f"{API_BASE}{endpoint}", params=params, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]:
        """Checks if the given project name or ID exists on Modrinth."""
        return ProjectAPI.request(f"/project/{slug_or_id}/check")

    @staticmethod
    def get_dependencies(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves all dependencies of a given project."""
        if ProjectAPI.is_slug_valid(project_name) is None:
            return None
        return ProjectAPI.request(f"/project/{project_name}/dependencies")

    @staticmethod
    def search_project(**kwargs) -> Optional[Dict[str, Any]]:
        """Searches for projects using various filters and sorting options."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        return ProjectAPI.request(f"/search", params=ProjectAPI.parse_url(params))

    @staticmethod
    def get_project(project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific project."""
        if ProjectAPI.is_slug_valid(project_name) is None:
            return None
        return ProjectAPI.request(f"/project/{project_name}")
    
    @staticmethod
    def get_projects(**kwargs) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific project."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        if any([ProjectAPI.is_slug_valid(project_name) for project_name in params["ids"]]):
            return None
        return ProjectAPI.request(f"/projects", params=ProjectAPI.parse_url(params))

    @staticmethod
    def list_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """Lists versions of a given project with optional filtering."""
        params = {k: v for k, v in kwargs.items() if v is not None and k != "project_name"}
        if ProjectAPI.is_slug_valid(kwargs["project_name"]) is None:
            return None
        return ProjectAPI.request(f"/project/{kwargs['project_name']}/version", params=ProjectAPI.parse_url(params))

    @staticmethod
    def get_version(version_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves information about a specific version by ID."""
        return ProjectAPI.request(f"/version/{version_id}")

    @staticmethod
    def get_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """Retrieves information about multiple versions by their IDs."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        return ProjectAPI.request(f"/versions", params=ProjectAPI.parse_url(params))

    