import modpack.mod as mod
from datetime import datetime
import json
import standard as std

# TODO Restructure json loading
class Modpack:
    title: str = "Modpack"
    description: str = "A modpack"
    build_date: str = datetime.today().strftime('%Y-%m-%d')
    build_version: str = "0.1"
    mc_version: str = "1.19"
    mod_loader: str = "fabric"
    mod_list: list[mod.Mod] = []
    flags: json = {"allow_alpha_beta": True}
    
    def __init__(self, **kwargs) -> None:
        """Constructor of modpack class"""
        for key in kwargs.keys():
            if key == 'mod_list':
                setattr(self, key, [mod.Mod(**item) for item in kwargs[key]])
            else:
                setattr(self, key, kwargs[key])
    
    def export_json(self) -> json:
        """Exports all variables in the current modpack object as a JSON object"""
        return json.loads(json.dumps(std.get_variables(self), cls=std.ProjectEncoder))

    def check_compatibility(self) -> bool:
        """Checks if the current mods are compatibel"""
        return True

    def get_mod_list_names(self) -> list:
        """Returns a list of all mod names"""
        return [f"{item.mod_name} - {item.mod_version}" for item in self.mod_list]
    