import requests, json
from . import *

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


    def search_project(self, project_name, facets, index, offset, limit) -> json:
        # Searches for a project using a name, facets, index, offset and limit
        if self.is_slug_valid(project_name) is None:
            return

        params = {'query': project_name, 'facets': json.dumps(facets), 'index': index, 'offset': offset, 'limit': limit}
        req = requests.get(SEARCH_PROJECT, json=params)
        if req.reason != 'OK':
            return
        return req.json()

    def get_project(self, project_name) -> json:
        # Returns 
        if self.is_slug_valid(project_name) is None:
            return

        req = requests.get(GET_PROJECT + project_name)
        if req.reason != 'OK':
            return
        return req.json()
    
    def get_projects(self, project_names) -> json:
        # Returns 
        for name in project_names:
            if self.is_slug_valid(name) is None:
                return
        params = {'ids': json.dumps(project_names)}
        print(params["ids"])
        req = requests.get(GET_PROJECTS, json=params)
        if req.reason != 'OK':
            return
        return req.json()




# data = r.json()
# print(data)