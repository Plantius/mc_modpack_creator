import json
import modpack_creator.standard as std

class mod:
    mod_name: str
    mod_version: str
    mc_version: str
    client_side: bool
    server_side: bool
    mod_loader: str
    id: str
    version: str

    def __init__(self, mod_name="A Mod", mod_version="1.0",
                 mc_version="1.21", client_side=True, server_side=True, 
                 mod_loader="Fabric", id="", version="") -> None:
        """Constructor of mod class"""
        self.mod_name = mod_name
        self.mod_version = mod_version
        self.mc_version = mc_version
        self.client_side = client_side
        self.server_side = server_side
        self.mod_loader = mod_loader
        self.id = id
        self.version = version


    def export_json(self):
        """Exports all variables in the current modpack object as a JSON object"""
        out_json = {"mod_name": self.mod_name, "mod_version": self.mod_version, "mc_version": self.mc_version,
               "client_side": self.client_side, "server_side": self.server_side, "mod_loader": self.mod_loader, 
               "id": self.id, "version": self.version}
        return json.loads(json.dumps(out_json))
    
    def load_json(self, in_json):
        # self = mod(**in_json)
        self.mod_name = in_json["mod_name"]
        self.mod_version = in_json["mod_version"]
        self.mc_version = in_json["mc_version"]
        self.client_side = in_json["client_side"]
        self.server_side = in_json["server_side"]
        self.mod_loader = in_json["mod_loader"]
        self.id = in_json["id"]
        self.version = in_json["version"]
 