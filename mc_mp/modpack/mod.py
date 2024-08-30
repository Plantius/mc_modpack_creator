import standard as std
from dataclasses import dataclass, field

@dataclass
class Mod:
    """
    Represents a mod with attributes and methods for JSON export and import.

    Attributes
    ----------
    mod_name : str
        The name of the mod. Defaults to "Mod".
    description : str
        A brief description of the mod. Defaults to "A mod".
    mod_version : str
        The version of the mod. Defaults to "1.0".
    dependencies : list
        A list of dependencies required by the mod. Defaults to an empty list.
    mc_versions : list
        A list of supported Minecraft versions. Defaults to ["1.19"].
    version_type : str
        The type of version (e.g., "release", "beta", "alpha"). Defaults to "release".
    client_side : str
        Specifies if the mod is required on the client side. Defaults to "required".
    server_side : str
        Specifies if the mod is required on the server side. Defaults to "optional".
    mod_loaders : list
        A list of mod loaders compatible with the mod. Defaults to an empty list.
    mod_id : str
        A unique identifier for the mod. Defaults to "IIJJKKLL".
    project_id : str
        A unique identifier for the project associated with the mod. Defaults to "AABBCCDD".
    date_published : str
        The date when the mod was published. Defaults to an empty string.
    files : list
        A list of files associated with the mod. Defaults to an empty list.

    Methods
    -------
    __init__(**kwargs) -> None
        Initializes the mod with the given attributes.
    export_json() -> dict
        Exports the mod's attributes as a JSON object.
    load_json(data: dict) -> None
        Loads the provided JSON data into the mod's attributes.
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

    # def __init__(self, **kwargs) -> None:
    #     """Initializes the mod with the given attributes."""
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def export_json(self) -> dict:
        """Exports the mod's attributes as a JSON object."""
        return std.get_variables(self)

    def load_json(self, data: dict) -> None:
        """Loads the provided JSON data into the mod's attributes."""
        for key, value in data.items():
            setattr(self, key, value)
