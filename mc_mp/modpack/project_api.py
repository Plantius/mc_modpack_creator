"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/project_api.py
Last Edited: 2024-09-07

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
import os
import logging
from aiohttp import ClientSession, ClientError
from typing import Optional, Dict, Any
from aiocache import cached
from mc_mp.constants import API_BASE, HEADERS, PROJECT_DIR

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class ProjectAPI:
    """Handles interactions with the Modrinth API for project-related data."""

    @staticmethod
    @cached(ttl=3600)
    async def request(endpoint: str, params: Dict[str, Any] = {}) -> Optional[Dict[str, Any]]:
        """
        Makes a GET request to the specified API endpoint and returns the JSON response.

        Args:
            endpoint (str): The API endpoint to query.
            params (Dict[str, Any]): Optional query parameters for the request.

        Returns:
            Optional[Dict[str, Any]]: The JSON response from the API, or None if the request fails.
        """
        async with ClientSession() as session:
            try:
                async with session.get(f"{API_BASE}{endpoint}", params=params, headers=HEADERS) as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientError as e:
                logger.error(f"[ERROR] Request to {API_BASE}{endpoint} failed: {e}")
                return None
            except Exception as e:
                logger.error(f"[ERROR] Unexpected error during request to {API_BASE}{endpoint}: {e}")
                return None

    @staticmethod
    def parse_url(params: Dict[str, Any]) -> str:
        """
        Converts a dictionary of parameters into a URL query string.

        Args:
            params (Dict[str, Any]): The dictionary of parameters to convert.

        Returns:
            str: A URL-friendly query string.
        """
        return '&'.join(f'{key}={value}' for key, value in params.items()).replace('\'', '\"').replace(" ", "")

    @staticmethod
    @cached(ttl=3600)
    async def is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]:
        """
        Checks if the given project slug or ID exists on Modrinth, with caching.

        Args:
            slug_or_id (str): The project slug or ID to validate.

        Returns:
            Optional[Dict[str, Any]]: The API response if the slug or ID is valid, or None if invalid.
        """
        try:
            return await ProjectAPI.request(f"/project/{slug_or_id}/check")
        except Exception as e:
            logger.error(f"[ERROR] Failed to validate slug or ID {slug_or_id}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_dependencies(project_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves all dependencies for the specified project, with caching.

        Args:
            project_name (str): The name of the project.

        Returns:
            Optional[Dict[str, Any]]: The list of dependencies, or None if an error occurs.
        """
        try:
            return await ProjectAPI.request(f"/project/{project_name}/dependencies")
        except Exception as e:
            logger.error(f"[ERROR] Failed to get dependencies for project {project_name}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def search_project(**kwargs) -> Optional[Dict[str, Any]]:
        """
        Searches for projects using various filters and sorting options, with caching.

        Args:
            **kwargs: Filter and search parameters for the project search.

        Returns:
            Optional[Dict[str, Any]]: The search results from the API, or None if the search fails.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request("/search", params=ProjectAPI.parse_url(params))
        except Exception as e:
            logger.error(f"[ERROR] Project search failed with parameters {params}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_project(project_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed information about a specific project.

        Args:
            project_name (str): The name of the project.

        Returns:
            Optional[Dict[str, Any]]: The project details, or None if an error occurs.
        """
        try:
            return await ProjectAPI.request(f"/project/{project_name}")
        except Exception as e:
            logger.error(f"[ERROR] Could not retrieve project {project_name}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_projects(**kwargs) -> Optional[Dict[str, Any]]:
        """
        Retrieves information about multiple projects using various filters, with caching.

        Args:
            **kwargs: Optional filter parameters for the project search.

        Returns:
            Optional[Dict[str, Any]]: The project data, or None if an error occurs.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request("/projects", params=ProjectAPI.parse_url(params))
        except KeyError as e:
            logger.error(f"[ERROR] Missing required key 'ids' in parameters: {e}")
            return None
        except Exception as e:
            logger.error(f"[ERROR] Failed to retrieve projects with parameters {params}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def list_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """
        Lists versions of a specified project with optional filtering.

        Args:
            **kwargs: Optional filter parameters for the version search.

        Returns:
            Optional[Dict[str, Any]]: The list of versions, or None if an error occurs.
        """
        try:
            params = {k: v for k, v in kwargs.items() if v is not None and k != "id"}
            return await ProjectAPI.request(f"/project/{kwargs['id']}/version", params=ProjectAPI.parse_url(params))
        except KeyError as e:
            logger.error(f"[ERROR] Missing required key 'id' in parameters: {e}")
            return None
        except Exception as e:
            logger.error(f"[ERROR] Failed to list versions for project {kwargs.get('id', 'unknown')}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_version(version_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed information about a specific version by its ID.

        Args:
            version_id (str): The ID of the version.

        Returns:
            Optional[Dict[str, Any]]: The version details, or None if an error occurs.
        """
        try:
            return await ProjectAPI.request(f"/version/{version_id}")
        except Exception as e:
            logger.error(f"[ERROR] Could not retrieve version {version_id}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_versions(**kwargs) -> Optional[Dict[str, Any]]:
        """
        Retrieves information about multiple versions by their IDs.

        Args:
            **kwargs: Optional filter parameters for the version search.

        Returns:
            Optional[Dict[str, Any]]: The version data, or None if an error occurs.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request("/versions", params=params)
        except Exception as e:
            logger.error(f"[ERROR] Failed to retrieve versions with parameters {params}: {e}")
            return None

    @staticmethod
    async def get_file_from_url(**kwargs) -> None:
        """
        Downloads a file from the given URL and saves it to a specified location.

        Args:
            **kwargs: File metadata including the URL and filename.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            async with ClientSession() as session:
                async with session.get(params["url"]) as response:
                    if response.status == 200:
                        data = await response.read()
                        os.makedirs(os.path.dirname(f'{PROJECT_DIR}/{params["filename"]}'), exist_ok=True)
                        with open(f'{PROJECT_DIR}/{params["filename"]}', "wb") as file:
                            file.write(data)
                    else:
                        logger.error(f"[ERROR] Failed to download file: Status code {response.status}")
        except KeyError as e:
            logger.error(f"[ERROR] Missing required file download parameters: {e}")
        except Exception as e:
            logger.error(f"[ERROR] Could not download file: {e}")
