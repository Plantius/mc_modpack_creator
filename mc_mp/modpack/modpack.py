import json
from datetime import datetime
from typing import List, Dict, Any
import modpack.mod as mod
import standard as std

class Modpack:
    """
    Represents a Minecraft modpack with attributes like title, description, 
    build date, version, Minecraft version, mod loader, and included mods. 

    Attributes
    ----------
    title : str
        The title of the modpack. Defaults to "Modpack".
    description : str
        A brief description of the modpack. Defaults to "A modpack".
    build_date : str
        The build date of the modpack in 'YYYY-MM-DD' format. Defaults to the current date.
    build_version : str
        The version of the modpack. Defaults to "0.1".
    mc_version : str
        The Minecraft version that the modpack is built for. Defaults to "1.19".
    mod_loader : str
        The mod loader used by the modpack (e.g., "fabric"). Defaults to "fabric".
    mod_list : List[mod.Mod]
        A list of `mod.Mod` objects included in the modpack. Defaults to an empty list.


    Methods
    -------
    __init__(**kwargs: Any) -> None
        Initializes the Modpack with optional parameters.

    export_json() -> Dict[str, Any]
        Exports the Modpack attributes as a JSON object.

    check_compatibility() -> bool
        Checks if the current mods in the modpack are compatible (always returns `True`).

    get_mod_list_names() -> List[str]
        Returns a list of all mod names and their versions.
    """

    title: str = "Modpack"
    description: str = "A modpack"
    build_date: str = datetime.today().strftime('%Y-%m-%d')
    build_version: str = "0.1"
    mc_version: str = "1.19"
    mod_loader: str = "fabric"
    mod_list: List[mod.Mod] = []

    def __init__(self, **kwargs: Any) -> None:
        """Initializes the Modpack with optional parameters."""
        for key, value in kwargs.items():
            if key == 'mod_list' and isinstance(value, list):
                setattr(self, key, [mod.Mod(**item) for item in value])
            else:
                setattr(self, key, value)

    def export_json(self) -> Dict[str, Any]:
        """Exports the Modpack attributes as a JSON object."""
        return json.loads(json.dumps(std.get_variables(self), cls=std.ProjectEncoder))

    def check_compatibility(self) -> bool:
        """Checks if the current mods in the modpack are compatible (always returns `True`)."""
        return True

    def get_mod_list_names(self) -> List[str]:
        """Returns a list of all mod names and their versions."""
        return [f"{item.mod_name} - {item.mod_version}" for item in self.mod_list]
