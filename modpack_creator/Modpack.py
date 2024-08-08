from . import Mod
from DateTime import DateTime


class modpack:
    def __init__(self, name="My Modpack", build_date=DateTime.time, build_version="1.0",
                 mc_version="1.21", mod_loader="Fabric", mod_list=[]) -> None:
        self.name = name
        self.build_date = build_date
        self.build_version = build_version
        self.mc_version = mc_version
        self.mod_loader = mod_loader
        self.mod_list = mod_list
    

    def add_mod(self, new_mod: Mod):
        if new_mod.mc_version is not self.mc_version:
            print("ERROR")