from . import Mod

class modpack:
    def __init__(self, name, build_date, build_version,
                 mc_version, mod_loader, mod_list) -> None:
        self.name = name
        self.build_date = build_date
        self.build_version = build_version
        self.mc_version = mc_version
        self.mod_loader = mod_loader
        self.mod_list = mod_list
    
    def add_mod(self, new_mod: Mod):
        if new_mod.mc_version is not self.mc_version:
            print("ERROR")