"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/modpack.py
Last Edited: 2024-09-07

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
import json
from datetime import datetime
from typing import List, Dict, Any
from mc_mp.modpack.mod import Mod, ProjectEncoder
import mc_mp.standard as std

class Modpack:
    title: str = "Modpack"
    description: str = "A modpack"
    build_date: str = datetime.today().strftime('%Y-%m-%d')
    build_version: str = "0.1"
    mc_version: str = "1.19"
    mod_loader: str = "fabric"
    client_side: str = "required"
    server_side: str = "optional"
    mod_data: list[Mod] = []

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if key == 'mod_data' and isinstance(value, list):
                setattr(self, key, [Mod(**item) for item in value])
            else:
                setattr(self, key, value)
        self._processing_mods: set = set()

    @std.sync_timing
    def export_json(self) -> Dict[str, Any]:
        return json.loads(json.dumps(std.get_variables(self), cls=ProjectEncoder))

    @std.sync_timing
    def check_compatibility(self) -> bool:
        return not std.has_duplicates([m.project_id for m in self.mod_data])

    @std.sync_timing
    def get_mods_name_ver(self) -> List[str]:
        return [f"{item.title} - {item.version_number}" for item in self.mod_data]

    @std.sync_timing
    def get_mods_descriptions(self) -> List[str]:
        return [item.description for item in self.mod_data]
    
    @std.sync_timing
    def sort_mods(self) -> None:
        self.mod_data.sort(key=lambda mod: mod.project_id)
