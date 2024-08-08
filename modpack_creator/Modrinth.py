import requests, json
from . import SEARCH_PROJECT, DEPENDENCIES, GET_PROJECT, CHECK, VERSION

class project:
    def __init__(self) -> None:
        pass

    def is_slug_valid(self, project_name) -> json:
        # Checks if the given project name (slug) exist
        # on Modrinth
        req = requests.get(GET_PROJECT + project_name + CHECK)
        if req.reason != 'OK':
            return
        return req.json()

    def get_dependencies(self, project_name) -> json:
        # Returns all dependencies of a given project
        if self.is_slug_valid(project_name) is None:
            return
        
        req = requests.get(GET_PROJECT + project_name + DEPENDENCIES)
        if req.reason != 'OK':
            return
        return req.json()


    def search_project(self, project_name=None, facets=None, index=None, offset=None, limit=None) -> json:
        # Searches for a project using a name, facets, index, offset and limit
        if self.is_slug_valid(project_name) is None:
            return

        params = {'query': project_name, 'facets': json.dumps(facets), 'index': index, 'offset': offset, 'limit': limit}
        req = requests.get(SEARCH_PROJECT, params==params)
        if req.reason != 'OK':
            return
        return req.json()

    def get_project(self, project_name) -> json:
        # Returns the project information
        if self.is_slug_valid(project_name) is None:
            return

        req = requests.get(GET_PROJECT + project_name)
        if req.reason != 'OK':
            return
        return req.json()
    
    def get_versions(self, project_name, loaders="fabric", game_versions="1.21", featured=False):
        # Returns a projects version list
        if self.is_slug_valid(project_name) is None:
            return
        params = {'loaders': loaders, 'game_versions': game_versions, 'featured': featured}
        req = requests.get(GET_PROJECT + project_name + VERSION, params=params)
        if req.reason != 'OK':
            return
        return req.json()

