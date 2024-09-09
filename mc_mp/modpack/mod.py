"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/modpack/mod.py
Last Edited: 2024-09-10

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from dataclasses import dataclass, field
import mc_mp.standard as std
import json

class ProjectEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling `mod.Mod` objects."""

    def default(self, obj):
        """Encode `mod.Mod` objects to JSON; use default encoder otherwise."""
        if isinstance(obj, Mod):
            return obj.export_json()
        return super().default(obj)


@dataclass
class Mod:
    title: str = "Mod"
    description: str = "This is a mod"
    name: str = "Mod 1.0.0"
    changelog: str = "Changes"
    version_number: str = "1.0"
    mc_versions: list = field(default_factory=lambda: ["1.19"])
    version_type: str = "release"
    mod_loaders: list = field(default_factory=list)
    mod_id: str = "IIJJKKLL"
    project_id: str = "AABBCCDD"
    date_published: str = ""
    dependencies: list[dict] = field(default_factory=list)
    files: list[dict] = field(default_factory=list)

    @std.sync_timing
    def export_json(self) -> dict:
        data = std.get_variables(self)
        for key in {'files', 'dependencies', 'mod_loaders', 'mc_versions'}:
            if key in data and isinstance(data[key], list):
                # Serialize lists of dictionaries to JSON strings
                data[key] = json.dumps(data[key])
        return data

    @std.sync_timing
    def load_json(self, data: dict) -> None:
        for key, value in data.items():
            if key in {'files', 'dependencies', 'mod_loaders', 'mc_versions'}:
                value = json.loads(value) if isinstance(value, str) else value
            setattr(self, key, value)

    @std.sync_timing
    def update_self(self, latest_version: dict, project_info: dict):
        self.name = latest_version.get("name", self.name)
        self.changelog = latest_version.get("changelog", self.changelog)
        self.version_number = latest_version.get("version_number", self.version_number)
        self.dependencies = latest_version.get("dependencies", self.dependencies)
        self.mc_versions = latest_version.get("game_versions", self.mc_versions)
        self.version_type = latest_version.get("version_type", self.version_type)
        self.mod_loaders = latest_version.get("loaders", self.mod_loaders)
        self.mod_id = latest_version.get("mod_id", self.mod_id)
        self.project_id = latest_version.get("project_id", self.project_id)
        self.date_published = latest_version.get("date_published", self.date_published)
        self.files = latest_version.get("files", self.files)
        self.title = project_info.get("title", self.title)
        self.description = project_info.get("description", self.description)
