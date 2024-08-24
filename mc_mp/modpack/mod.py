import json
import standard as std

# TODO Restructure to accept json data better
class Mod:
    mod_name: str
    description: str
    mod_version: str
    dependencies: list
    mc_versions: list
    version_type: str
    client_side: str
    server_side: str
    mod_loaders: list
    mod_id: str
    project_id: str
    date_published: str
    files: list

    def __init__(self, **kwargs) -> None:
        """Constructor of mod class"""
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        # self.mod_name = mod_name
        # self.description = description
        # self.mod_version = mod_version
        # self.mc_version = mc_version
        # self.client_side = client_side
        # self.server_side = server_side
        # self.mod_loader = mod_loader
        # self.id = id
        # self.version = version
        # self.files = files


    def export_json(self):
        """Exports all variables in the current modpack object as a JSON object"""
        # out_json = {"mod_name": self.mod_name, "description": self.description, "mod_version": self.mod_version, "mc_version": self.mc_version,
        #        "client_side": self.client_side, "server_side": self.server_side, "mod_loader": self.mod_loader, 
        #        "id": self.id, "version": self.version, "files": self.files}
        return json.loads(json.dumps(std.get_variables(self)))
    
    def load_json(self, in_json):
        """Loads the given json into the class' variables"""
        for key in in_json.keys():
            setattr(self, key, in_json[key])
        # self.mod_name = in_json["mod_name"]
        # self.description = in_json["description"]
        # self.mod_version = in_json["mod_version"]
        # self.mc_version = in_json["mc_version"]
        # self.client_side = in_json["client_side"]
        # self.server_side = in_json["server_side"]
        # self.mod_loader = in_json["mod_loader"]
        # self.id = in_json["id"]
        # self.version = in_json["version"]
        # self.files = in_json["files"]
 