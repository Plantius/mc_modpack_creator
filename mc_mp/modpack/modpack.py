import modpack.mod as mod
from datetime import datetime
import json

# TODO Restructure json loading
class Modpack:
    title: str
    description: str
    build_date: datetime = datetime.today().strftime('%Y-%m-%d')
    build_version: str
    mc_version: str
    mod_loader: str
    mod_list: list[mod.Mod]
    flags: json
    
    def __init__(self, title="Modpack", description="My modpack", build_date=datetime.today().strftime('%Y-%m-%d'), build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[], flags={"allow_alpha_beta": True}) -> None:
        """Constructor of modpack class"""
        self.title = title
        self.description = description
        self.build_date = build_date
        self.build_version = build_version
        self.mc_version = mc_version
        self.mod_loader = mod_loader
        self.mod_list = [mod.Mod(**x) if type(x) is not mod.Mod else x for x in mod_list]
        self.flags = flags
    
    def export_json(self) -> json:
        """Exports all variables in the current modpack object as a JSON object"""
        out_json = {"title": self.title, "description": self.description, "build_date": self.build_date, "build_version": self.build_version,
               "mc_version": self.mc_version, "mod_loader": self.mod_loader, "mod_list": [mod.export_json() for mod in self.mod_list], "flags": self.flags}
        return json.loads(json.dumps(out_json))

    def check_compatibility(self) -> bool:
        """Checks if the current mods are compatibel"""
        return True

    def get_mod_list_names(self) -> list:
        """Returns a list of all mod names"""
        return [x.mod_name for x in self.mod_list]

    def add_mod(self, new_mod: mod.Mod):
        if new_mod.mc_version is not self.mc_version:
            print("Error: this mod does not match the current minecraft version.")