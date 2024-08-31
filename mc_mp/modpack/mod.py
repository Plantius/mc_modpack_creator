"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/mod.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
import standard as std
from dataclasses import dataclass, field

@dataclass
class Mod:
    """
    Represents a mod with attributes and methods for JSON serialization and deserialization.
    """

    title: str = "Mod"
    description: str = "This is a mod"
    name: str = "Mod 1.0.0"
    changelog: str = "Changes"
    version_number: str = "1.0"
    dependencies: list[dict] = field(default_factory=list)
    mc_versions: list = field(default_factory=lambda: ["1.19"])
    version_type: str = "release"
    mod_loaders: list = field(default_factory=list)
    id: str = "IIJJKKLL"
    project_id: str = "AABBCCDD"
    date_published: str = ""
    files: list[dict] = field(default_factory=list)

    def export_json(self) -> dict:
        """Exports the mod's attributes as a JSON-compatible dictionary."""
        return std.get_variables(self)

    def load_json(self, data: dict) -> None:
        """Loads JSON data into the mod's attributes."""
        for key, value in data.items():
            setattr(self, key, value)
