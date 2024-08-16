import modpack_creator.Mod as Mod
from datetime import datetime
import json


class modpack:
    name: str
    build_date: datetime
    build_version: str
    mc_version: str
    mod_loader: str
    mod_list: list
    compatibel: bool
    
    def __init__(self, name="My Modpack", build_date=datetime.today().strftime('%Y-%m-%d'), build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[]) -> None:
        """Constructor of modpack class"""
        self.name = name
        self.build_date = build_date
        self.build_version = build_version
        self.mc_version = mc_version
        self.mod_loader = mod_loader
        self.mod_list = mod_list
    
    def export_json(self) -> json:
        """Exports all variables in the current modpack object as a JSON object"""
        out_json = {"name": self.name, "build_date": self.build_date, "build_version": self.build_version,
               "mc_version": self.mc_version, "mod_loader": self.mod_loader, "mod_list": [mod.export_json() for mod in self.mod_list],
               "compatibel": self.compatibel}
        return json.loads(json.dumps(out_json))

    def check_compatibility(self) -> bool:
        return True

    def add_mod(self, new_mod: Mod):
        if new_mod.mc_version is not self.mc_version:
            print("Error: this mod does not match the current minecraft version.")