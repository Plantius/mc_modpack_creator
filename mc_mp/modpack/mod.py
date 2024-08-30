import standard as std
from dataclasses import dataclass, field

@dataclass
class Mod:
    """
    Represents a mod with various attributes and methods to handle JSON serialization and deserialization.

    Attributes:
    ------------
    title : str
        The title of the mod (default is "Mod").
    description : str
        A brief description of the mod (default is "This is a mod").
    name : str
        The name of the mod version (default is "Mod 1.0.0").
    changelog : str
        A description of the changes in the current mod version (default is "Changes").
    version_number : str
        The version number of the mod (default is "1.0").
    dependencies : list[dict]
        A list of dictionaries representing the mod's dependencies (default is an empty list).
    mc_versions : list[str]
        A list of supported Minecraft versions (default is ["1.19"]).
    version_type : str
        The type of the mod's version (e.g., "release", "beta", "alpha") (default is "release").
    client_side : str
        Specifies if the mod is required on the client side (default is "required").
    server_side : str
        Specifies if the mod is required on the server side (default is "optional").
    mod_loaders : list[str]
        A list of mod loaders that are compatible with this mod (default is an empty list).
    mod_id : str
        A unique identifier for the mod (default is "IIJJKKLL").
    project_id : str
        A unique identifier for the associated project (default is "AABBCCDD").
    date_published : str
        The date the mod was published (default is an empty string).
    files : list[str]
        A list of files associated with the mod (default is an empty list).

    Methods:
    ---------
    __init__(**kwargs) -> None
        Initializes a new instance of the Mod class with the provided attributes.
    export_json() -> dict
        Exports the mod's attributes as a JSON-compatible dictionary.
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

    def export_json(self) -> dict:
        """Exports the mod's attributes as a JSON object."""
        return std.get_variables(self)

    def load_json(self, data: dict) -> None:
        """Loads the provided JSON data into the mod's attributes."""
        for key, value in data.items():
            setattr(self, key, value)
