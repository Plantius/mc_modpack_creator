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
    """
    Represents a Minecraft modpack with various attributes and methods for managing mods.
    """

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
        """
        Initializes the Modpack with optional parameters.

        Args:
            kwargs (Any): Optional parameters for initializing the modpack attributes.
        """
        for key, value in kwargs.items():
            if key == 'mod_data' and isinstance(value, list):
                setattr(self, key, [Mod(**item) for item in value])
            else:
                setattr(self, key, value)
        self._processing_mods: set = set()

    @std.sync_timing
    def export_json(self) -> Dict[str, Any]:
        """
        Exports the Modpack attributes as a JSON-compatible dictionary.

        Returns:
            dict: The Modpack's attributes serialized as a dictionary.
        """
        return json.loads(json.dumps(std.get_variables(self), cls=ProjectEncoder))

    @std.sync_timing
    def check_compatibility(self) -> bool:
        """
        Checks if the mods in the modpack are compatible.

        Returns:
            bool: True if there are no duplicate mods, otherwise False.
        """
        return not std.has_duplicates([m.project_id for m in self.mod_data])

    @std.sync_timing
    def get_mods_name_ver(self) -> List[str]:
        """
        Returns a list of all mod names and their version numbers.

        Returns:
            List[str]: List of mod names with their version numbers.
        """
        return [f"{item.title} - {item.version_number}" for item in self.mod_data]

    @std.sync_timing
    def get_mods_descriptions(self) -> List[str]:
        """
        Returns a list of all mod descriptions.

        Returns:
            List[str]: List of mod descriptions.
        """
        return [item.description for item in self.mod_data]
    
    @std.sync_timing
    def sort_mods(self) -> None:
        """
        Sorts the mod_data list by mod title.
        """
        self.mod_data.sort(key=lambda mod: mod.project_id)
