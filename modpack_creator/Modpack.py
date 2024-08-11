from . import Mod
from datetime import datetime
import json


class modpack:
    name: str
    build_date: datetime
    build_version: str
    mc_version: str
    mod_loader: str
    mod_list: list
    def __init__(self, name="My Modpack", build_date=datetime.today().strftime('%Y-%m-%d'), build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[]) -> None:
        self.name = name
        self.build_date = build_date
        self.build_version = build_version
        self.mc_version = mc_version
        self.mod_loader = mod_loader
        self.mod_list = mod_list
    
    def export_json(self) -> json:
        out_json = {"name": self.name, "build_date": self.build_date, "build_version": self.build_version,
               "mc_version": self.mc_version, "mod_loader": self.mod_loader, "mod_list": [mod.export_json() for mod in self.mod_list]}
        return json.loads(json.dumps(out_json))

    def save_project(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.export_json()))

    def add_mod(self, new_mod: Mod):
        if new_mod.mc_version is not self.mc_version:
            print("ERROR")