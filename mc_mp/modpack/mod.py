"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/mod.py
Last Edited: 2024-09-07

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
            
    def update_self(self, latest_version: dict, project_info: dict):
        """Updates the mod's attributes with the latest version and project information."""
        self.name = latest_version["name"]
        self.changelog = latest_version["changelog"]
        self.version_number = latest_version["version_number"]
        self.dependencies = latest_version["dependencies"]
        self.mc_versions = latest_version["game_versions"]
        self.version_type = latest_version.get("version_type", self.version_type)
        self.mod_loaders = latest_version["loaders"]
        self.id = latest_version["id"]
        self.project_id = latest_version["project_id"]
        self.date_published = latest_version["date_published"]
        self.files = latest_version["files"]
        self.title = project_info.get("title", self.title)
        self.description = project_info.get("description", self.description)
