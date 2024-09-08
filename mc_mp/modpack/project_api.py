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
    @staticmethod
    @cached(ttl=3600)
    async def request(endpoint: str, params: Dict[str, Any] = {}) -> Optional[Dict[str, Any]]:
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
        return '&'.join(f'{key}={value}' for key, value in params.items()).replace('\'', '\"').replace(" ", "")

    @staticmethod
    @cached(ttl=3600)
    async def is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]:
        try:
            return await ProjectAPI.request(f"/project/{slug_or_id}/check")
        except Exception as e:
            logger.error(f"[ERROR] Failed to validate slug or ID {slug_or_id}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_dependencies(project_name: str) -> Optional[Dict[str, Any]]:
        try:
            return await ProjectAPI.request(f"/project/{project_name}/dependencies")
        except Exception as e:
            logger.error(f"[ERROR] Failed to get dependencies for project {project_name}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def search_project(**kwargs) -> Optional[Dict[str, Any]]:
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request("/search", params=ProjectAPI.parse_url(params))
        except Exception as e:
            logger.error(f"[ERROR] Project search failed with parameters {params}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_project(project_name: str) -> Optional[Dict[str, Any]]:
        try:
            return await ProjectAPI.request(f"/project/{project_name}")
        except Exception as e:
            logger.error(f"[ERROR] Could not retrieve project {project_name}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_projects(**kwargs) -> Optional[Dict[str, Any]]:
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
        try:
            return await ProjectAPI.request(f"/version/{version_id}")
        except Exception as e:
            logger.error(f"[ERROR] Could not retrieve version {version_id}: {e}")
            return None

    @staticmethod
    @cached(ttl=3600)
    async def get_versions(**kwargs) -> Optional[Dict[str, Any]]:
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            return await ProjectAPI.request("/versions", params=params)
        except Exception as e:
            logger.error(f"[ERROR] Failed to retrieve versions with parameters {params}: {e}")
            return None

    @staticmethod
    async def get_file_from_url(**kwargs) -> None:
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
