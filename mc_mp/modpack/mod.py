import json
import standard as std

# TODO Restructure to accept json data better
class Mod:
    mod_name: str = "Mod"
    description: str = "A mod"
    mod_version: str = "1.0"
    dependencies: list = []
    mc_versions: list = ["1.19"]
    version_type: str = "release"
    client_side: str = "required"
    server_side: str = "optional"
    mod_loaders: list = []
    mod_id: str = "IIJJKKLL"
    project_id: str = "AABBCCDD"
    date_published: str = ""
    files: list = []

    def __init__(self, **kwargs) -> None:
        """Constructor of mod class"""
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def export_json(self):
        """Exports all variables in the current modpack object as a JSON object"""
        return json.loads(json.dumps(std.get_variables(self), cls=std.ProjectEncoder))
    
    def load_json(self, in_json):
        """Loads the given json into the class' variables"""
        for key in in_json.keys():
            setattr(self, key, in_json[key])
      
 