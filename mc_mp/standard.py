import sys, inspect, json
from cryptography.fernet import Fernet
import modpack.mod as mod

SECRET_KEY: bytes = "_Wentk-C_UTgkPQlUKoXQy_QGncHXgm8RoC4-ddWBG8="
MAGIC: bytes = b"MODPACK_PROJECT_CREATOR"

ALLOWED_CATEGORIES = ["forge", "fabric", "neoforge", "quilt", "liteloader"]

class ProjectEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for handling `mod.Mod` objects.

    This encoder extends the `json.JSONEncoder` to provide custom serialization 
    for `mod.Mod` objects. When an object of type `mod.Mod` is encountered, 
    it uses the `export_json` method of the `mod.Mod` class to convert the 
    object to a JSON-serializable format. For other types of objects, it uses 
    the default serialization provided by `json.JSONEncoder`.

    Methods
    -------
    default(obj: Any) -> Any
        Override of the default method to handle custom JSON encoding for `mod.Mod` objects.
    """

    def default(self, obj):
        """Encode `mod.Mod` objects to JSON; use default encoder otherwise."""
        if isinstance(obj, mod.Mod):
            return obj.export_json()
        return super().default(obj)


def get_variables(obj) -> dict:
    """Get non-callable attributes of an object as a dictionary."""
    return {key: value for key, value in inspect.getmembers(obj) 
            if not callable(getattr(obj, key)) and not key.startswith("__")}

def get_functions(obj) -> list:
    """Get a list of callable methods, excluding special methods."""
    return [name for name in dir(obj) 
            if callable(getattr(obj, name)) and not name.startswith("__")]

def generate_id() -> str:
    """Generate and return a base64-encoded encrypted ID."""
    f = Fernet(SECRET_KEY)
    return f.encrypt(MAGIC).decode("utf-8")

def check_id(id: str) -> bool:
    """Check if the provided ID matches the encrypted value."""
    f = Fernet(SECRET_KEY)
    try:
        return f.decrypt(id.encode("utf-8")) == MAGIC
    except (ValueError, TypeError):
        return False

def get_input(msg: str) -> str:
    """Prompt for ASCII input and return it if valid."""
    inp = input(msg)
    if not inp.isascii() or inp is None:
        eprint("[ERROR] Input must be a non-empty ASCII string.")
        return None
    return inp

def get_index(lst: list, item) -> int:
    """Return the index of an item in the list, or `None` if not found."""
    try:
        return lst.index(item)
    except ValueError:
        return None

def eprint(*args, **kwargs) -> None:
    """Print errors to standard error."""
    print(*args, file=sys.stderr, **kwargs)
