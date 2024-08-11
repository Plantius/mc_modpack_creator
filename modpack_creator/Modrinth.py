import requests, json
from . import Modpack
from datetime import datetime
from . import API_BASE, HEADERS

class project:
    def __init__(self, name="My Modpack", build_date=datetime.today().strftime('%Y-%m-%d'), build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[]) -> None:
        self.mp = Modpack.modpack(name, build_date, build_version, mc_version, mod_loader, mod_list)

    def is_slug_valid(self, project_name) -> json:
        # Checks if the given project name (slug) exist
        # on Modrinth
        req = requests.get(API_BASE + '/project/' + project_name + '/check', headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

    def get_dependencies(self, project_name) -> json:
        # Returns all dependencies of a given project
        if self.is_slug_valid(project_name) is None:
            return
        
        req = requests.get(API_BASE + '/project/' + project_name + '/dependencies', headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

    def search_project(self, name="", facets="", index="relevance", offset=0, limit=10) -> json:
        # Searches for a project using a name, facets, index, offset and limit
        
        params = {'query': name, 'facets': f'[{",".join([f"{x}" for x in facets])}]', 'index': index, 'offset': offset, 'limit': limit}
        par_url = '&'.join([f'{x}={params[x]}' for x in params.keys()]).replace('\'', '\"')
        print(par_url)
        req = requests.get(API_BASE + '/search', params=par_url, headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

    def get_project(self, project_name) -> json:
        # Returns the project information
        if self.is_slug_valid(project_name) is None:
            return

        req = requests.get(API_BASE + '/project/' + project_name, headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()
    
    def list_versions(self, project_name, loaders="", game_versions="", featured=True):
        # Returns a projects version list
        if self.is_slug_valid(project_name) is None:
            return
        params = {'loaders': f'[{",".join([f"{x}" for x in loaders])}]', 'game_versions': f'[{",".join([f"{x}" for x in game_versions])}]', 'featured': featured}
        par_url = '&'.join([f'{x}={params[x]}' for x in params.keys()]).replace('\'', '\"')

        print(json.dumps(params))
        print(params)
        req = requests.get(API_BASE + '/project/' + project_name + '/version', params=par_url, headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

