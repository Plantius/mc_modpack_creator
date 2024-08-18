import requests, json
import modpack.modpack as modpack
from datetime import datetime
from . import API_BASE, HEADERS



class Project:
    mp: modpack.Modpack
    loaded: bool
    saved: bool
    valid: bool
    filename: str
    
    def __init__(self, name="Modpack", description="My Modpack", build_date=datetime.today().strftime('%Y-%m-%d'), build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[], loaded=False, saved=True, valid=False, filename="project1.json") -> None:
        """Constructor of project class"""
        self.loaded = False
        self.saved = True
        self.valid = True
        self.filename = "project1.json"
    
    def create_project(self, name="Modpack", description="My modpack", build_date=datetime.today().strftime('%Y-%m-%d'), build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[], loaded=True, saved=False, valid=False) -> None:
        """Create a new project"""
        self.mp = modpack.Modpack(name, description, build_date, build_version, mc_version, mod_loader, mod_list)
        self.loaded = loaded
        self.saved = saved
        self.valid = self.mp.check_compatibility()
        if self.valid is not True:
            print("Invalid project created.")
            exit(1)

    def load_project(self, filename: str) -> None:
        """Loads the given project file """
        with open(filename, 'r') as file:
            file_json = json.loads(file.read())
            self.mp = modpack.Modpack(**file_json)
            self.loaded = file_json["loaded"]
            self.saved = file_json["saved"]
            self.valid = file_json["valid"]
            self.filename = filename
            if self.valid is not True:
                print("Invalid project loaded.")
                exit(1)

    def save_project(self, filename):
        with open(filename, 'w') as file:
            self.filename = filename
            flags = {"loaded": self.loaded, "saved": True, "valid": self.valid, "filename": filename}
            out_json = {**self.mp.export_json(), **flags}
            file.write(json.dumps(out_json, indent=1))
    
    def parse_url(self, dic) -> str:
        """Parses a dictionary to a correct parameter string"""
        return '&'.join([f'{x}={dic[x]}' for x in dic.keys()]).replace('\'', '\"')


    def is_slug_valid(self, slug_or_id: str) -> json:
        """Checks if the given project name (slug) or ID exist on Modrinth"""
        req = requests.get(API_BASE + '/project/' + slug_or_id + '/check', headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

    def get_dependencies(self, project_name: str) -> json:
        """Returns all dependencies of a given project"""
        if self.is_slug_valid(project_name) is None:
            return
        
        req = requests.get(API_BASE + '/project/' + project_name + '/dependencies', headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

    def search_project(self, **kwargs) -> json:
        """Searches for a project using a name, facets, index, offset and limit.
        \nArguments are:\n
            query: The query to search for
            facets: Used to filter out results
            index: The sorting method used for sorting search results ("relevance" "downloads" "follows" "newest" "updated")
            offset: The offset into the search. Skips this number of results
            limit: The number of results returned by the search
        """
        params = {}
        for i in kwargs.items():
            if i[-1] != None:
                params[i[0]] = i[-1]
        print(params)
        req = requests.get(API_BASE + '/search', params=self.parse_url(params), headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()

    def get_project(self, project_name: str) -> json:
        """Returns the project information"""
        if self.is_slug_valid(project_name) is None:
            return

        req = requests.get(API_BASE + '/project/' + project_name, headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()
    
    def list_versions(self, project_name: str, **kwargs) -> json:
        """Returns a projects version list
        \n Arguments are:\n
            loaders: The types of loaders to filter for
            game_versions: The game versions to filter for
            featured: Allows to filter for featured or non-featured versions only
        """
        params = {}
        if self.is_slug_valid(project_name) is None:
            return
        for i in kwargs.items():
            if i[-1] != None:
                params[i[0]] = i[-1]
        # params = {'loaders': join_list(loaders), 'game_versions': join_list(game_versions), 'featured': featured}

        req = requests.get(API_BASE + '/project/' + project_name + '/version', params=self.parse_url(params), headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()
    
    def get_version(self, version_id: str) -> json:
        """Returns the specified version"""
        req = requests.get(API_BASE + '/version/' + version_id, headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()
    
    def get_versions(self, ids: str) -> json:
        """Returns the specified versions"""
        params = {'ids': ids}

        req = requests.get(API_BASE + '/versions', params=self.parse_url(params), headers=HEADERS)
        if req.reason != 'OK':
            return
        return req.json()
    

